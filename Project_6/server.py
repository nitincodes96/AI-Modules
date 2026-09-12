"""
Local MCP server for the capstone app.
Exposes a real weather tool backed by the OpenWeather API, over STDIO.

Run standalone for testing:  uv run server.py
Needs OPENWEATHER_API_KEY in the environment (loaded from .env).

Works on both MCP SDK versions:
  - mcp 2.x:  from mcp.server.mcpserver import MCPServer
  - mcp 1.x:  from mcp.server.fastmcp import FastMCP
This app uses 2.x because the Airbnb server requires it.
"""
import os
import requests
from dotenv import load_dotenv


load_dotenv(".env")
try:
    # MCP SDK 2.x (FastMCP was renamed to MCPServer)
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:
    # MCP SDK 1.x fallback
    from mcp.server.fastmcp import FastMCP as _Server

mcp = _Server("Weather")

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@mcp.tool()
def get_weather(city: str) -> str:
    """Gets the current weather for a city using the OpenWeather API.
    city should be a plain city name, for example 'Delhi' or 'London'."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "OPENWEATHER_API_KEY is not set on the server."
    try:
        params = {"q": city, "appid": api_key, "units": "metric"}
        resp = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        if resp.status_code == 404:
            return f"City '{city}' not found."
        resp.raise_for_status()
        data = resp.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        name = data.get("name", city)
        country = data.get("sys", {}).get("country", "")
        return (
            f"Weather in {name}, {country}: {desc}. "
            f"Temperature {temp} C (feels like {feels} C), "
            f"humidity {humidity}%, wind {wind} m/s."
        )
    except Exception as e:
        return f"Error fetching weather for {city}: {e}"


@mcp.tool()
def add_note_to_file(content: str) -> str:
    """
    Appends the given content to the user's local notes.
    Args:
        content: The text content to append.
    """

    filename = 'notes.txt'

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Content appended to {filename}."
    except Exception as e:
        return f"Error appending to file {filename}: {e}"
    

@mcp.tool()
def read_notes() -> str:
    """
    Reads and returns the contents of the user's local notes.
    """
    filename = 'notes.txt'

    try:
        with open(filename, "r", encoding="utf-8") as f:
            notes = f.read()
        return notes if notes else "No notes found."
    except FileNotFoundError:
        return "No notes file found."
    except Exception as e:
        return f"Error reading file {filename}: {e}"

    """
    Capture the current screen and return the image. Use this tool whenever the user requests a screenshot of their activity.
    """

    buffer = io.BytesIO()

    # if the file exceeds ~1MB, it will be rejected by Claude
    screenshot = pyautogui.screenshot()
    screenshot.convert("RGB").save(buffer, format="JPEG", quality=60, optimize=True)
    return Image(data=buffer.getvalue(), format="jpeg")
if __name__ == "__main__":
    mcp.run()
