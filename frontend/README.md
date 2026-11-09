# Frontend run instructions

This is a Vite + React application; do not open `index.html` directly in a browser.

```powershell
cd frontend
npm install
npm run dev
```

Open the exact `http://localhost:xxxx/` address printed by Vite. Keep the FastAPI backend running at `http://localhost:8000` in a separate terminal. If the frontend cannot start, it will now render a visible error message rather than a blank screen.
