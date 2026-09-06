import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

# Google Calendar API imports
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# LangChain & LangGraph imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY missing from .env file.")
    st.stop()

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# --- 1. Google Calendar Service Initialization ---
def get_calendar_service():
    """Authenticates using credentials.json and returns the Google Calendar API service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError("credentials.json not found in project directory.")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

try:
    calendar_service = get_calendar_service()
except Exception as e:
    st.error(f"Google Calendar Authentication Error: {e}")
    st.stop()

# --- 2. Live Calendar Tools ---
@tool
def check_availability(date: str) -> str:
    """
    Check scheduled events on Google Calendar for a specific date.
    Args:
        date: The target date formatted strictly as 'YYYY-MM-DD'.
    """
    try:
        start_of_day = f"{date}T00:00:00Z"
        end_of_day = f"{date}T23:59:59Z"

        events_result = calendar_service.events().list(
            calendarId="primary",
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return f"No events found on {date}. The entire day is free."

        busy_summary = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            title = event.get("summary", "Busy")
            busy_summary.append(f"'{title}' from {start} to {end}")

        return f"Scheduled events on {date}:\n" + "\n".join(busy_summary)
    except Exception as err:
        return f"Error querying Google Calendar: {str(err)}"

@tool
def book_calendar(title: str, start_iso: str, end_iso: str, description: str = "") -> str:
    """
    Create a new event on Google Calendar.
    Args:
        title: Title/summary of the meeting.
        start_iso: Event start time in ISO 8601 format (e.g., '2026-09-07T14:00:00+05:30').
        end_iso: Event end time in ISO 8601 format (e.g., '2026-09-07T15:00:00+05:30').
        description: Optional notes or meeting agenda.
    """
    try:
        event_body = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_iso},
            "end": {"dateTime": end_iso}
        }
        created_event = calendar_service.events().insert(
            calendarId="primary",
            body=event_body
        ).execute()

        return f"Success! Event created: '{created_event.get('summary')}' at {start_iso}. Link: {created_event.get('htmlLink')}"
    except Exception as err:
        return f"Failed to schedule event: {str(err)}"

tools = [check_availability, book_calendar]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

# --- 3. LangGraph Architecture ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot_node(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph = graph_builder.compile()

# --- Saving Graph as Image ---
try:
    with open("agent_architecture.png", "wb") as f:
        f.write(graph.get_graph().draw_mermaid_png())
    print("Graph image saved successfully.")
except Exception as e:
    print(f"Could not save graph image: {e}")

# --- 4. Streamlit UI ---
st.set_page_config(page_title="Google Calendar Agent", page_icon="📅")
st.title("📅 Agentic Google Calendar Manager")

with st.sidebar:
    st.success("Connected to Google Calendar API")
    st.info("The agent reads and writes directly to your primary calendar account.")

if "messages" not in st.session_state:
    # Dynamically inject current system time to prevent date hallucination
    live_time = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    
    st.session_state.messages = [
        SystemMessage(content=f"You are a calendar management AI. Today's date and current local time is {live_time}. Use this exact time to accurately calculate relative dates like 'tomorrow' or 'next Tuesday'. When generating ISO 8601 timestamps, assume the user's local timezone unless specified otherwise."),
        AIMessage(content="Hello! I am synced with your Google Calendar. Ask me to verify availability or book a meeting.")
    ]

# Render conversation history (SystemMessages are hidden from the UI)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage) and msg.content:
        st.chat_message("assistant").write(msg.content)

# Process user prompt
if user_prompt := st.chat_input("E.g., Check my schedule for tomorrow or book a 30-minute sync at 3 PM."):
    st.chat_message("user").write(user_prompt)
    st.session_state.messages.append(HumanMessage(content=user_prompt))

    with st.spinner("Analyzing calendar and executing actions..."):
        events = graph.stream({"messages": st.session_state.messages})

        for event in events:
            for node_name, state_update in event.items():
                latest_msg = state_update["messages"][-1]
                st.session_state.messages.append(latest_msg)

                # Only output final reasoning/text to the user, not tool payloads
                if isinstance(latest_msg, AIMessage) and latest_msg.content:
                    st.chat_message("assistant").write(latest_msg.content)