# MicroBiz Copilot

AI-powered business intelligence and payment operations for small businesses.

This repository is a starter scaffold for a portfolio project. It includes a React + Vite frontend and a FastAPI backend health endpoint. The analytics, AI tools, database, and PayPal sandbox integration are planned next steps—not implemented yet.

## Prerequisites

- Python 3.11+ recommended
- Node.js 20+ recommended
- npm

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check: http://127.0.0.1:8000/health

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will print the local URL, usually http://localhost:5173.

## Project structure

- `frontend/` — React + Vite UI
- `backend/app/` — FastAPI application
- `backend/tests/` — backend tests
- `docs/` — project notes

## Security notes

- Never commit `.env` files, API keys, PayPal client secrets, or real customer/payment data.
- Use PayPal sandbox credentials only during development.
- Do not treat browser-provided payment amounts or statuses as authoritative.
- Verify PayPal webhook signatures before processing events.
- The AI must use approved backend tools; do not expose unrestricted SQL or payment credentials to the model.

## Planned milestones

1. Working frontend/backend skeleton
2. Database models and seeded demo data
3. Deterministic sales analytics
4. AI copilot with controlled tools
5. PayPal sandbox checkout and verified webhooks
6. Tests, documentation, and deployment
