# Project_4 — Interactive Dynamic RAG Knowledge Base

## Problem

In many AI applications, knowledge bases are hardcoded or pre-indexed by developers. This is highly impractical for real-world users who need to analyze their own constantly changing documents (manuals, policies, reports) on the fly.

If an employee needs to quickly find a specific termination clause in a newly drafted contract, they cannot wait for a developer to update the app's backend. Furthermore, if a user attempts to ask the AI questions before their files are fully processed and indexed, the system will either crash or confidently hallucinate answers based on its general training data rather than the user's actual documents.

Build a Streamlit-based dynamic RAG application that can:

1. Provide a runtime file upload interface (e.g., TXT or PDF) alongside a **"Build Knowledge Base"** trigger.
2. Prevent user chatting prior to building the knowledge base by keeping the chat interface completely hidden or disabled.
3. Ingest and chunk the uploaded documents on demand using dynamic text splitters.
4. Index chunks into ChromaDB with metadata (such as source filename or chunk IDs) using OpenAI embeddings.
5. Unlock an interactive chat interface once the knowledge base is successfully created.
6. Retrieve the most relevant chunks dynamically and answer user queries strictly grounded in the uploaded context.

## Setup Instructions
1. Initialize the Python environment and install dependencies: `uv add -r requirements.txt`
2. Configure your `.env` file with your vector database and model API keys.