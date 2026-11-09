from fastapi.testclient import TestClient
from uuid import uuid4
from app.main import app


def test_copilot_is_grounded():
    with TestClient(app) as client:
        response = client.post("/api/copilot/chat", json={"message": "Which orders need attention?"})
    body = response.json()
    assert response.status_code == 200
    assert body["grounded"] is True
    assert body["tool"] == "list_orders_needing_attention"


def test_duplicate_webhook_is_idempotent():
    with TestClient(app) as client:
        event = {"event_id": f"test-event-{uuid4()}", "event_type": "PAYMENT.CAPTURE.COMPLETED"}
        first = client.post("/api/webhooks/paypal", json=event)
        second = client.post("/api/webhooks/paypal", json=event)
    assert first.json()["processed"] is True
    assert second.json()["duplicate"] is True
