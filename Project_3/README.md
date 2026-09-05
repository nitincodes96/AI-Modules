# Project_3 — AI Customer Support Agent

## Problem

Small online businesses receive many repetitive customer-support questions such as:

- "Where is my order?"
- "Can I return my product?"
- "Is my order eligible for a refund?"
- "Why hasn't my order arrived?"
- "Can I cancel my order?"

A basic chatbot may answer these questions incorrectly because it does not have access to actual order information and may simply guess.

Your task is to build an **AI Customer Support Agent** using **Python, OpenAI, and Streamlit**.

The agent should understand the customer's request, use a tool to retrieve order information when required, follow store policies, and return a useful response.


## Objective

Build a Streamlit-based AI support assistant that can:

1. Understand customer questions.
2. Identify when order information is required.
3. Use a tool to retrieve information from a mock order database.
4. Apply predefined store policies.
6. Return a customer-friendly response.
7. Return a structured action that another system could use.

## Objective

Build a Streamlit-based AI support assistant that can:

1. Understand customer questions.
2. Identify when order information is required.
3. Use a tool to retrieve information from a mock order database.
4. Apply predefined store policies.
5. Never invent order information.
6. Return a customer-friendly response.
7. Return a structured action that another system could use.

## Modules Used

### `openai`
The official Python client for interacting with the OpenAI API. We use it to send prompts, pass tools to the model, and request structured data.

### `pydantic`
A data validation library. We use it to define strict "schemas" (like the `SupportDecision` class) that force the AI to return data in the exact format our application expects (JSON with specific keys and data types).

### `python-dotenv`
A utility library that reads key-value pairs from a `.env` file and sets them as environment variables. This is crucial for keeping our `OPENAI_API_KEY` secure and out of the source code.

### `streamlit`
A framework for rapidly building web applications for data science and AI projects. We use it to create the user interface, handle chat history, and display the backend system outputs side-by-side with the conversation.

## Setup Instructions
1. Install dependencies: `uv add -r requirements.txt` (or `uv add openai python-dotenv streamlit`)
2. Create a `.env` file with your `OPENAI_API_KEY="sk-..."`
3. Run the app: `uv run streamlit run main.py`