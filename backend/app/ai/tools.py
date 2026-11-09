from datetime import date
from app.services.analytics import compare_sales_periods, orders_needing_attention, sales_summary


def get_sales_summary(start: date, end: date) -> dict:
    return sales_summary(start, end)


def compare_periods(start: date, end: date) -> dict:
    return compare_sales_periods(start, end)


def list_orders_needing_attention() -> dict:
    return {"orders": orders_needing_attention(), "count": len(orders_needing_attention())}


TOOLS = {
    "get_sales_summary": get_sales_summary,
    "compare_sales_periods": compare_periods,
    "list_orders_needing_attention": list_orders_needing_attention,
}
