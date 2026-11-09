# MicroBiz architecture

```text
React UI ──REST──> FastAPI routes ──> services ──> SQLite
                       │                 │
                       │                 ├── analytics (deterministic reporting)
                       │                 ├── Copilot tool registry (allow-list)
                       │                 └── payment adapter ──> PayPal sandbox
                       └── webhook verifier ──> idempotent event store
```

## Source of truth

The UI never computes revenue. The analytics service sums integer paise from `payments.status = 'CAPTURED'`; returned totals include their reporting period. The Copilot can only invoke named functions in `ai/tools.py` and is given their structured output. It cannot access SQL, secrets, or arbitrary HTTP endpoints.

## Payment lifecycle

`CREATED → APPROVED → CAPTURED` is modelled separately from `FAILED`, `PENDING`, and `REFUNDED`. Only `CAPTURED` is revenue. A later verified refund event changes its payment state and appears as a separate refund metric. `webhook_events.event_id` is unique, so repeat delivery is harmless.

## PayPal production checklist

Use server-held sandbox/live credentials, create and capture orders server-side, verify every webhook with PayPal's verification endpoint, compare captured amount/currency to the local order, and never accept browser-provided totals. The included adapter is intentionally local-demo only until those credentials are configured.
