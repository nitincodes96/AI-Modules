"""
FastAPI backend for the multi-server MCP chat app.

Opens both MCP servers for the duration of each request, using the same
nested-context pattern as the course's multi-server client. This keeps the
async contexts on one task (which MCP's stdio client requires) and is the
most reliable way to use several servers behind a web API.

  - "weather" : the local server (server.py), real OpenWeather data
  - "airbnb"  : the community Airbnb server, run via npx (no API key)

Run:  uvicorn backend:app --reload
"""
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from models import ChatRequest, ChatResponse
from agent import run_agent

load_dotenv(".env")
assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env"

WEATHER = StdioServerParameters(command=sys.executable, args=["server.py"])
AIRBNB = StdioServerParameters(
    command="npx", args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
)

app = FastAPI(title="MCP Chat App (Weather + Airbnb)")


async def _with_sessions(fn):
    """Open both servers, run fn(sessions), then close them, all on one task."""
    async with stdio_client(WEATHER) as (r1, w1), stdio_client(AIRBNB) as (r2, w2):
        async with ClientSession(r1, w1) as weather, ClientSession(r2, w2) as airbnb:
            await weather.initialize()
            await airbnb.initialize()
            sessions = {"weather": weather, "airbnb": airbnb}
            return await fn(sessions)


@app.get("/tools")
async def list_tools():
    async def work(sessions):
        out = {}
        for name, session in sessions.items():
            result = await session.list_tools()
            out[name] = [t.name for t in result.tools]
        return out
    return await _with_sessions(work)


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    async def work(sessions):
        answer, tools_used = await run_agent(sessions, req.query)
        return ChatResponse(answer=answer or "", tools_used=tools_used)
    return await _with_sessions(work)


@app.get("/health")
async def health():
    # Lightweight: does not open the servers.
    return {"status": "ok", "servers": ["weather", "airbnb"]}
