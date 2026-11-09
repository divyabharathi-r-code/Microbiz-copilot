# MicroBiz Copilot

An evidence-first operations console for small businesses. The dashboard is calculated on the server, the Copilot uses an allow-listed tool layer, and consequential payment follow-ups remain review-only.

## What is included

- React + Vite operations console with dashboard, orders, payment follow-ups, and Copilot.
- FastAPI + SQLite API with seeded demo transactions in INR paise.
- Deterministic reporting for captured revenue, refunds, open orders, and daily trends.
- A grounded Copilot adapter: it recognizes a small set of questions, calls a controlled tool, and renders an answer from the returned figures. It has no SQL or credential access.
- A sandbox-payment boundary: orders can be created and captured through the backend; swap `app/integrations/paypal.py` to use live PayPal sandbox credentials.
- Idempotent webhook-event storage and audit logs.

## Run locally

Open two terminals from this folder.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
uvicorn app.main:app --reload --port 8000
```

```powershell
cd frontend
npm install
npm run dev
```

Visit the URL Vite prints (normally `http://localhost:5173`). The API docs are at `http://localhost:8000/docs`.

## Verification

```powershell
cd backend
pytest -q
```

## Integrity rules

Only `CAPTURED` payments contribute to revenue. Pending, authorized, failed, and refunded payments do not. Refunds remain separately visible. The generated demo data is marked as sandbox data, and no action is sent without an explicit owner approval request.

## Project map

- `backend/app/services/analytics.py` — authoritative money calculations
- `backend/app/ai/tools.py` — registered, validated Copilot tools
- `backend/app/services/copilot.py` — intent routing and grounded prose
- `backend/app/integrations/paypal.py` — payment-provider boundary
- `docs/architecture.md` — request flow and security model
