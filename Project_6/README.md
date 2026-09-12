# MCP Chat App (Streamlit + FastAPI + MCP)

A complete, runnable chat app. A Streamlit UI talks over HTTP to a FastAPI
backend, which connects to two MCP servers and runs an OpenAI agent loop:

- **weather** - a local MCP server (server.py) backed by the real OpenWeather API
- **airbnb**  - the community Airbnb MCP server, run via npx (no API key needed)

Ask for a weather report or an Airbnb search in plain language; the agent picks
the right tool from the right server.

    Streamlit UI  ->  FastAPI backend  ->  weather + airbnb MCP servers  ->  tools
       app.py           backend.py           server.py / npx

## Files

- server.py        Local MCP server: get_weather (OpenWeather API)
- models.py        Pydantic ChatRequest / ChatResponse
- agent.py         Multi-server agent loop: combine tools, route each call
- backend.py       FastAPI; opens both servers per request, exposes /tools, /chat, /health
- app.py           Streamlit front end
- mcp.json         Reference config for the Airbnb server
- pyproject.toml / requirements.txt
- .env.example     copy to .env and add your keys

## Setup

Prerequisites: Python 3.10+, and Node.js (for `npx`, used by the Airbnb server).

    uv venv
    # Windows:  .venv\Scripts\activate
    # macOS/Linux:  source .venv/bin/activate
    uv pip install -r requirements.txt

Then add your keys:

    cp .env.example .env
    # edit .env:
    #   OPENAI_API_KEY=sk-...
    #   OPENWEATHER_API_KEY=...   (from openweathermap.org)

## Run

Two terminals (both with the venv active).

Terminal 1, the backend:

    uvicorn backend:app --reload

Terminal 2, the UI:

    streamlit run app.py

Open the Streamlit URL (usually http://localhost:8501) and try:

- "What's the weather in Delhi?"
- "Find me an Airbnb in Goa for 2 guests."

## Notes

- **First Airbnb call is slow.** `npx` downloads the Airbnb server the first time,
  so the first request can take 30-60s. After that it is cached and quick.
- **MCP version.** This app uses `mcp[cli]>=2`. The Airbnb server requires the
  2.x protocol. In 2.x, `FastMCP` was renamed to `MCPServer`; server.py imports
  whichever is available, so it also runs on 1.x if you ever pin back.
- **Sessions are opened per request** (the reliable pattern for several MCP
  servers behind a web API). For a single always-on server you could instead
  open it once at startup.
- **Security.** Keep keys in .env (never commit it). .gitignore already excludes it.

## Make it yours

- Add a tool: write another `@mcp.tool()` in server.py. It appears automatically.
- Add a server: add its StdioServerParameters in backend.py and include it in the
  sessions dict. The agent routes calls to whichever server owns each tool.
- Swap the model: change "gpt-4o" in agent.py. The MCP side is unchanged.

## Notebook

MCP_Chat_App_Walkthrough.ipynb builds the project cell by cell and runs the
MCP + agent loop live in the notebook.
