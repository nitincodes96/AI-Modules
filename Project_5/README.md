# Project 5 — Agentic Google Calendar Manager

## The Problem
Scheduling meetings manually is a tedious, multi-step process. When a user asks a standard AI to "set up a meeting with Sarah tomorrow afternoon," it fails. Standard LLMs lack the ability to execute sequential actions, interact with live external environments, or maintain the complex state required for multi-turn scheduling negotiations.

## The Solution
This project builds an **Agentic Calendar Manager** using LangGraph, OpenAI, and Streamlit. The AI transitions from a passive chatbot into a stateful agent that can independently execute tools. It checks your live Google Calendar for free slots, reasons about the available times, proposes a slot to the user, and securely books the appointment directly to your account.

## Features
* **Stateful Graph Execution:** Uses LangGraph to manage cyclical decision-making between the LLM and calendar tools.
* **Live API Integration:** Reads and writes directly to Google Calendar using OAuth 2.0.
* **Temporal Awareness:** Injects live system time into the agent's context to accurately resolve relative dates (e.g., "tomorrow at 3 PM").
* **Architecture Visualization:** Automatically generates a Mermaid PNG diagram of the LangGraph state machine upon compilation.

---

## How to Get Your `credentials.json`
To allow the agent to read and write to your Google Calendar, you must generate an OAuth 2.0 Client ID from Google Cloud.

**Step 1: Create a Google Cloud Project**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown in the top left and select **New Project**. Name it (e.g., "Calendar Agent") and click **Create**.

**Step 2: Enable the Calendar API**
1. In the left sidebar, navigate to **APIs & Services > Library**.
2. Search for **Google Calendar API** and click **Enable**.

**Step 3: Configure the OAuth Consent Screen**
1. Navigate to **APIs & Services > OAuth consent screen**.
2. Choose **External** (unless you have a Google Workspace org) and click **Create**.
3. Fill out the required fields (App Name, User Support Email, Developer Contact Email). You can skip the optional fields.
4. On the **Scopes** screen, just click Save and Continue.
5. On the **Test Users** screen, click **Add Users** and enter the Google email address you will use to test the calendar. 

**Step 4: Generate the Credentials**
1. Navigate to **APIs & Services > Credentials**.
2. Click **Create Credentials** at the top and select **OAuth client ID**.
3. Set the Application type to **Desktop app**. Name it and click **Create**.
4. A modal will appear. Click **Download JSON**.
5. Move this downloaded file into your project's root folder and rename it exactly to `credentials.json`.

---

## Setup & Execution

**1. Install Dependencies**
Using `uv`, initialize your environment and install the required packages:
```bash
uv add -r requirements.txt