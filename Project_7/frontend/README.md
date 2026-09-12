# Portfolio — Frontend

React + Vite + Tailwind CSS portfolio with an embedded AI chat widget.

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # production build in dist/
```

The chat widget calls `http://localhost:8000/api/chat` by default. Override with `VITE_API_URL` in a `.env` file (see `.env.example`).

Replace `public/resume.pdf` with your real resume — the **Download Resume** button links to it.
