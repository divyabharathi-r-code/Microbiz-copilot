from datetime import date
from app.core.db import init_db
from app.services.analytics import compare_sales_periods, sales_summary


def setup_module():
    init_db()


def test_captured_revenue_excludes_pending_failed_and_refunded():
    summary = sales_summary(date(2026, 10, 27), date(2026, 11, 2))
    assert summary["captured_sales_paise"] == 369700
    assert summary["refunds_paise"] == 129900
    assert summary["captured_payment_count"] == 3


def test_comparison_uses_same_length_periods():
    result = compare_sales_periods(date(2026, 10, 27), date(2026, 11, 2))
    assert result["current"]["period"] == {"start": "2026-10-27", "end": "2026-11-02", "timezone": "UTC"}
    assert result["previous"]["period"]["start"] == "2026-10-20"
