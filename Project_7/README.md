# Nitin Kumar Singh — Portfolio + AI Assistant

Dark-themed developer portfolio (React + Vite + Tailwind) with an embedded chat assistant backed by FastAPI + OpenAI.

```
Project_7/
├── backend/    FastAPI service — POST /api/chat
└── frontend/   Vite React app — portfolio UI + ChatBot widget
```

## Run locally

**Backend** (terminal 1)
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # add your OPENAI_API_KEY
uvicorn main:app --reload --port 8000
```

**Frontend** (terminal 2)
```bash
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

The widget calls `http://localhost:8000/api/chat`. CORS allows `http://localhost:5173` by default (`ALLOWED_ORIGINS` in backend `.env`).

## Customising
- Portfolio content: `frontend/src/data/profile.js`
- Assistant knowledge: `backend/context.py` (keep both in sync)
- Resume: replace `frontend/public/resume.pdf`
- Project links: fill in `live` / `repo` in `profile.js` — the **Live** button enables itself once a URL is set
