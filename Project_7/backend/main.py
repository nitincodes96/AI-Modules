import logging
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)
from pydantic import BaseModel, Field

from context import SYSTEM_PROMPT

# Project-local backend/.env wins; then fall back to any .env found in parent directories.
load_dotenv(Path(__file__).with_name(".env"))
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("portfolio-api")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini").strip() or "gpt-4o-mini"
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    if o.strip()
]
MAX_HISTORY = 20  # trailing turns forwarded to the model

# Placeholder value from .env.example counts as "not configured".
_key_configured = bool(OPENAI_API_KEY) and OPENAI_API_KEY != "your_openai_api_key_here"
client = OpenAI(api_key=OPENAI_API_KEY) if _key_configured else None
if not _key_configured:
    log.warning("OPENAI_API_KEY is not set — /api/chat will return 503 until it is configured.")

app = FastAPI(title="Portfolio Assistant API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: list[HistoryMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def root():
    return {"status": "ok", "model": MODEL_NAME, "configured": _key_configured}


@app.get("/api/health")
def health():
    return {"status": "ok", "configured": _key_configured}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="The assistant isn't configured yet (missing OPENAI_API_KEY on the server).",
        )

    message = req.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="Message cannot be empty.")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += [m.model_dump() for m in req.history[-MAX_HISTORY:]]
    messages.append({"role": "user", "content": message})

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.4,
            max_tokens=400,
        )
    except AuthenticationError:
        log.error("OpenAI rejected the API key.")
        raise HTTPException(status_code=503, detail="The assistant's API key is invalid.")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="The assistant is busy right now — please try again in a moment.")
    except APIConnectionError:
        log.exception("Could not reach OpenAI.")
        raise HTTPException(status_code=502, detail="Could not reach the language model service.")
    except APIStatusError as e:
        log.error("OpenAI API error %s: %s", e.status_code, e.message)
        raise HTTPException(status_code=502, detail="The language model returned an error.")

    reply = (completion.choices[0].message.content or "").strip()
    if not reply:
        reply = "Sorry, I couldn't come up with a reply. Could you rephrase that?"
    return ChatResponse(reply=reply)
