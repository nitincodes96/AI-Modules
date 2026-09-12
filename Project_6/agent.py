"""
The agent loop for a multi-server setup.

Given a dict of {server_name: open ClientSession}, it:
  1. lists tools from every server and remembers which server owns each tool,
  2. hands the combined tool list to the LLM,
  3. routes each tool call to the session that owns that tool,
  4. feeds the results back and returns the final answer.

Same pattern as the course's client_query.py, extended to many servers.
"""
import json
from openai import OpenAI

# Created on first use so the app can boot before a key is needed.
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


async def collect_tools(sessions: dict):
    """List tools from every session. Returns (openai_tools, owner_by_tool)."""
    openai_tools = []
    owner_by_tool = {}
    for name, session in sessions.items():
        result = await session.list_tools()
        for tool in result.tools:
            owner_by_tool[tool.name] = name
            openai_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema,
                    },
                }
            )
    return openai_tools, owner_by_tool


async def run_agent(sessions: dict, query: str):
    """Run one query across all servers. Returns (answer, tools_used)."""
    tools_used = []
    openai_tools, owner_by_tool = await collect_tools(sessions)

    messages = [{"role": "user", "content": query}]

    response = _get_client().chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=openai_tools,
        tool_choice="auto",
    )
    messages.append(response.choices[0].message)

    if response.choices[0].message.tool_calls:
        for call in response.choices[0].message.tool_calls:
            tool_name = call.function.name
            tools_used.append(tool_name)
            # route the call to the server that owns this tool
            owner = owner_by_tool.get(tool_name)
            session = sessions[owner]
            result = await session.call_tool(
                tool_name,
                arguments=json.loads(call.function.arguments),
            )
            text = result.content[0].text if result.content else ""
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": text,
                }
            )
    else:
        return response.choices[0].message.content, tools_used

    final = _get_client().chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=openai_tools,
        tool_choice="auto",
    )
    return final.choices[0].message.content, tools_used
