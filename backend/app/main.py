from datetime import date, datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import connection, init_db
from app.integrations.paypal import create_sandbox_order, verify_webhook
from app.schemas.models import CaptureRequest, ChatRequest, CreateOrderRequest, DateRange, ReminderRequest
from app.services.analytics import dashboard_summary, list_orders, orders_needing_attention, sales_summary
from app.services.copilot import answer

app = FastAPI(title="MicroBiz Copilot API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@app.get("/health")
def health():
    return {"ok": True, "environment": "sandbox"}


@app.get("/api/dashboard/summary")
def get_dashboard_summary():
    # Demo data is anchored on this display date; production uses date.today().
    return dashboard_summary(date(2026, 11, 2))


@app.get("/api/analytics/sales")
def sales(start: date, end: date):
    range_ = DateRange(start=start, end=end)
    return sales_summary(range_.start, range_.end)


@app.get("/api/orders")
def get_orders():
    return {"items": list_orders(), "total": len(list_orders())}


@app.post("/api/orders", status_code=201)
def create_order(payload: CreateOrderRequest):
    with connection() as conn:
        cur = conn.execute("INSERT INTO orders(customer_email,status,total_paise,created_at) VALUES (?, 'PENDING_PAYMENT', ?, ?)", (payload.customer_email, payload.total_paise, now()))
        order_id = cur.lastrowid
        conn.execute("INSERT INTO audit_logs(actor,action,created_at) VALUES ('owner','created_demo_order',?)", (now(),))
    return {"id": order_id, **payload.model_dump(), "status": "PENDING_PAYMENT", "environment": "sandbox"}


@app.post("/api/payments/paypal/create-order")
def create_paypal_order(payload: CreateOrderRequest):
    payment_order = create_sandbox_order(payload.total_paise)
    with connection() as conn:
        cur = conn.execute("INSERT INTO orders(customer_email,status,total_paise,created_at) VALUES (?, 'PENDING_PAYMENT', ?, ?)", (payload.customer_email, payload.total_paise, now()))
        order_id = cur.lastrowid
        conn.execute("INSERT INTO payments(order_id,paypal_order_id,status,amount_paise,created_at) VALUES (?,?, 'PENDING', ?, ?)", (order_id, payment_order["id"], payload.total_paise, now()))
    return {"order_id": order_id, "paypal": payment_order}


@app.post("/api/payments/paypal/capture")
def capture_paypal_order(payload: CaptureRequest):
    with connection() as conn:
        row = conn.execute("SELECT o.total_paise, p.paypal_order_id, p.status FROM orders o JOIN payments p ON p.order_id=o.id WHERE o.id=?", (payload.order_id,)).fetchone()
        if not row or row["paypal_order_id"] != payload.paypal_order_id:
            raise HTTPException(404, "A matching server-created payment was not found")
        if row["status"] == "CAPTURED":
            raise HTTPException(409, "Payment has already been captured")
        capture_id = f"CAP-SANDBOX-{payload.order_id}"
        conn.execute("UPDATE payments SET status='CAPTURED', capture_id=? WHERE order_id=?", (capture_id, payload.order_id))
        conn.execute("UPDATE orders SET status='PAID' WHERE id=?", (payload.order_id,))
        conn.execute("INSERT INTO audit_logs(actor,action,created_at) VALUES ('owner','captured_sandbox_payment',?)", (now(),))
    return {"order_id": payload.order_id, "capture_id": capture_id, "status": "CAPTURED", "amount_verified_paise": row["total_paise"]}


@app.post("/api/webhooks/paypal")
def paypal_webhook(payload: dict):
    if not verify_webhook(payload):
        raise HTTPException(400, "Webhook verification failed")
    with connection() as conn:
        seen = conn.execute("SELECT 1 FROM webhook_events WHERE event_id=?", (payload["event_id"],)).fetchone()
        if seen:
            return {"processed": False, "duplicate": True}
        conn.execute("INSERT INTO webhook_events(event_id,event_type,processed_at) VALUES (?,?,?)", (payload["event_id"], payload["event_type"], now()))
    return {"processed": True, "duplicate": False}


@app.post("/api/copilot/chat")
def chat(payload: ChatRequest):
    return answer(payload.message, date(2026, 11, 2))


@app.get("/api/reminders/eligible")
def eligible_reminders():
    return {"items": orders_needing_attention()}


@app.post("/api/reminders/draft")
def draft_reminder(payload: ReminderRequest):
    order = next((x for x in orders_needing_attention() if x["id"] == payload.order_id), None)
    if not order:
        raise HTTPException(422, "Only pending or failed-payment orders are eligible for a reminder")
    amount = order["total_paise"] / 100
    return {"order_id": order["id"], "requires_owner_approval": True, "channel": "not_sent", "draft": f"Hello, a payment of ₹{amount:,.0f} for your MicroBiz order is still outstanding. Please let us know if you need a new payment link. Thank you."}
