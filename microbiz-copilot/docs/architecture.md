# MicroBiz Copilot — Architecture Notes

## MVP goals

- Show accurate business metrics calculated by backend code.
- Answer owner questions using a small allowlist of AI tools.
- Demonstrate a PayPal sandbox checkout flow.
- Keep owner approval in the loop for consequential actions.

## Initial request flow

1. React frontend sends requests to FastAPI.
2. FastAPI validates input and calls business services.
3. Business services read/write application data.
4. AI orchestration may call explicitly registered tools.
5. PayPal operations are performed server-side where required.
6. Verified webhook events update payment state idempotently.

## Planned domain entities

- User
- Product
- Order
- OrderItem
- Payment
- WebhookEvent
- AuditLog

## Important invariants

- Only successfully captured payments count toward captured sales.
- Store money as integer minor units (for example, paise) where practical.
- Never trust client-submitted payment totals or statuses.
- Verify webhook authenticity and process each event idempotently.
- Keep credentials server-side and exclude `.env` from version control.
- The model must not run arbitrary SQL or perform payment actions autonomously.
