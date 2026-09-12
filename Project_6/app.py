"""
Streamlit front end. Speaks plain HTTP to the FastAPI backend, never MCP directly.

Run (after the backend is up):  streamlit run app.py
"""
import requests
import streamlit as st

API = "http://localhost:8000"

st.set_page_config(page_title="MCP Chat App", page_icon="💬")
st.title("MCP Chat App")
st.caption("Streamlit UI  ->  FastAPI  ->  Weather + Airbnb MCP servers")

if "history" not in st.session_state:
    st.session_state["history"] = []

with st.sidebar:
    st.header("Connected servers")
    try:
        tools = requests.get(f"{API}/tools", timeout=15).json()
        st.success("Backend connected")
        for server, names in tools.items():
            st.markdown(f"**{server}**")
            for t in names:
                st.markdown(f"- `{t}`")
    except Exception:
        st.error("Backend not reachable. Start it with:")
        st.code("uvicorn backend:app --reload")
    if st.button("Reset chat"):
        st.session_state["history"] = []
        st.rerun()
    st.divider()
    st.caption("Try: \"What's the weather in Delhi?\" or "
               "\"Find me an Airbnb in Goa for 2 guests.\"")

query = st.text_input("Ask something", key="query")

if st.button("Send") and query:
    with st.spinner("Thinking..."):
        try:
            r = requests.post(f"{API}/chat", json={"query": query}, timeout=180)
            data = r.json()
            st.session_state["history"].append(
                (query, data.get("answer", ""), data.get("tools_used", []))
            )
        except Exception as e:
            st.error(f"Request failed: {e}")

for user, bot, used in reversed(st.session_state["history"]):
    st.markdown(f"**You:** {user}")
    st.markdown(f"**AI:** {bot}")
    if used:
        st.caption("Tools used: " + ", ".join(used))
    st.divider()
