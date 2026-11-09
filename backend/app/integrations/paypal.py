"""Provider boundary. This local adapter deliberately never touches real PayPal."""
from uuid import uuid4


def create_sandbox_order(amount_paise: int) -> dict:
    return {"id": f"PAYPAL-SANDBOX-{uuid4().hex[:12].upper()}", "status": "CREATED", "amount_paise": amount_paise, "environment": "sandbox"}


def verify_webhook(payload: dict) -> bool:
    # Replace with PayPal's server-side verification API before enabling real callbacks.
    return bool(payload.get("event_id") and payload.get("event_type"))
