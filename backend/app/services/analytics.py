from datetime import date, timedelta
from app.core.db import connection


def _period(start: date, end: date) -> dict:
    return {"start": start.isoformat(), "end": end.isoformat(), "timezone": "UTC"}


def sales_summary(start: date, end: date) -> dict:
    """The canonical sales calculation: only captured payments are revenue."""
    with connection() as conn:
        captured = conn.execute("""
          SELECT COALESCE(SUM(p.amount_paise),0) amount, COUNT(*) count
          FROM payments p JOIN orders o ON o.id=p.order_id
          WHERE p.status='CAPTURED' AND date(p.created_at) BETWEEN ? AND ?
        """, (start.isoformat(), end.isoformat())).fetchone()
        refunds = conn.execute("""
          SELECT COALESCE(SUM(p.amount_paise),0) amount, COUNT(*) count FROM payments p
          WHERE p.status='REFUNDED' AND date(p.created_at) BETWEEN ? AND ?
        """, (start.isoformat(), end.isoformat())).fetchone()
    return {"period": _period(start, end), "currency": "INR", "captured_sales_paise": captured["amount"], "captured_payment_count": captured["count"], "refunds_paise": refunds["amount"], "refund_count": refunds["count"]}


def compare_sales_periods(start: date, end: date) -> dict:
    length = (end - start).days + 1
    prior_end = start - timedelta(days=1)
    prior_start = prior_end - timedelta(days=length - 1)
    current, prior = sales_summary(start, end), sales_summary(prior_start, prior_end)
    change = current["captured_sales_paise"] - prior["captured_sales_paise"]
    percent = None if prior["captured_sales_paise"] == 0 else round(change / prior["captured_sales_paise"] * 100, 1)
    return {"current": current, "previous": prior, "change_paise": change, "change_percent": percent}


def dashboard_summary(today: date) -> dict:
    week_start = today - timedelta(days=6)
    summary = sales_summary(week_start, today)
    with connection() as conn:
        pending = conn.execute("SELECT COUNT(*) FROM orders WHERE status='PENDING_PAYMENT'").fetchone()[0]
        trend_rows = conn.execute("""
          SELECT date(created_at) day, COALESCE(SUM(amount_paise),0) amount
          FROM payments WHERE status='CAPTURED' AND date(created_at) BETWEEN ? AND ? GROUP BY date(created_at)
        """, (week_start.isoformat(), today.isoformat())).fetchall()
    amounts = {r["day"]: r["amount"] for r in trend_rows}
    trend = [{"date": (week_start + timedelta(days=i)).isoformat(), "amount_paise": amounts.get((week_start + timedelta(days=i)).isoformat(), 0)} for i in range(7)]
    return {**summary, "pending_orders": pending, "daily_sales": trend, "environment": "sandbox"}


def orders_needing_attention() -> list[dict]:
    with connection() as conn:
        rows = conn.execute("""
          SELECT o.id, o.customer_email, o.status, o.total_paise, o.created_at, o.due_at, p.status payment_status
          FROM orders o LEFT JOIN payments p ON p.order_id=o.id
          WHERE o.status IN ('PENDING_PAYMENT','PAYMENT_FAILED') ORDER BY o.created_at ASC
        """).fetchall()
    return [dict(r) for r in rows]


def list_orders() -> list[dict]:
    with connection() as conn:
        rows = conn.execute("""
          SELECT o.id, o.customer_email, o.status, o.total_paise, o.created_at, o.environment, p.status payment_status
          FROM orders o LEFT JOIN payments p ON p.order_id=o.id ORDER BY o.created_at DESC
        """).fetchall()
    return [dict(r) for r in rows]
