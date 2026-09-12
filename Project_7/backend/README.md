# Portfolio — Backend

FastAPI service that powers the portfolio chat widget.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then add your OPENAI_API_KEY
uvicorn main:app --reload --port 8000
```

- `POST /api/chat` — `{"message": "...", "history": [{"role": "user"|"assistant", "content": "..."}]}` → `{"reply": "..."}`
- `GET  /api/health` — reports whether an API key is configured

Without a valid key the server still starts; `/api/chat` returns `503` with a friendly message that the frontend displays.
