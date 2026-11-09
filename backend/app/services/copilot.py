from datetime import date, timedelta
from app.ai.tools import TOOLS


def rupees(paise: int) -> str:
    return f"₹{paise / 100:,.0f}"


def answer(message: str, today: date) -> dict:
    """A replaceable, deterministic MVP orchestrator. All figures come from tool output."""
    normalized = message.lower()
    start = today - timedelta(days=6)
    end = today
    if any(token in normalized for token in ("attention", "unpaid", "pending", "failed order", "need attention")):
        result = TOOLS["list_orders_needing_attention"]()
        count = result["count"]
        prose = f"I found {count} order{'s' if count != 1 else ''} needing attention. These are pending or failed payments; none are counted as captured sales."
        return {"answer": prose, "tool": "list_orders_needing_attention", "data": result, "grounded": True}
    if any(token in normalized for token in ("compare", "last week", "week over", "changed")):
        result = TOOLS["compare_sales_periods"](start, end)
        change = result["change_paise"]
        if result["change_percent"] is None:
            prose = f"Captured sales this week are {rupees(result['current']['captured_sales_paise'])}. There is no prior captured-sales baseline for a percentage comparison."
        else:
            direction = "increased" if change >= 0 else "decreased"
            prose = f"Captured sales {direction} from {rupees(result['previous']['captured_sales_paise'])} to {rupees(result['current']['captured_sales_paise'])} ({abs(result['change_percent']):g}%)."
        return {"answer": prose, "tool": "compare_sales_periods", "data": result, "grounded": True}
    result = TOOLS["get_sales_summary"](start, end)
    prose = f"Captured sales for {result['period']['start']} to {result['period']['end']} are {rupees(result['captured_sales_paise'])} across {result['captured_payment_count']} captured payment(s). Refunds shown separately: {rupees(result['refunds_paise'])}."
    return {"answer": prose, "tool": "get_sales_summary", "data": result, "grounded": True}
