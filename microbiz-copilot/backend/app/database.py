
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "microbiz.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                customer TEXT NOT NULL,
                item TEXT NOT NULL,
                amount_paise INTEGER NOT NULL,
                payment_status TEXT NOT NULL,
                refund_paise INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert demo records only when the table is empty.
        count = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

        if count == 0:
            demo_orders = [
                ("MB-1048", "Aarav S.", "Handmade gift box", 125000, "captured", 0),
                ("MB-1047", "Meera K.", "Ceramic coffee mug", 65000, "pending", 0),
                ("MB-1046", "Rohan P.", "Cotton tote bag", 48000, "captured", 0),
                ("MB-1045", "Isha R.", "Desk planter", 92000, "captured", 85000),
            ]

            connection.executemany("""
                INSERT INTO orders
                (id, customer, item, amount_paise, payment_status, refund_paise)
                VALUES (?, ?, ?, ?, ?, ?)
            """, demo_orders)


def get_dashboard_summary():
    with get_connection() as connection:
        row = connection.execute("""
            SELECT
                COALESCE(SUM(
                    CASE WHEN payment_status = 'captured'
                    THEN amount_paise ELSE 0 END
                ), 0) AS captured_sales_paise,

                SUM(CASE WHEN payment_status = 'captured'
                    THEN 1 ELSE 0 END) AS completed_payments,

                SUM(CASE WHEN payment_status = 'pending'
                    THEN 1 ELSE 0 END) AS pending_orders,

                COALESCE(SUM(refund_paise), 0) AS refunds_paise
            FROM orders
        """).fetchone()

    return {
        "captured_sales": row["captured_sales_paise"] / 100,
        "completed_payments": row["completed_payments"],
        "pending_orders": row["pending_orders"],
        "refunds": row["refunds_paise"] / 100,
        "source": "sqlite_demo_database",
    }


def get_recent_orders():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, customer, item, amount_paise, payment_status
            FROM orders
            ORDER BY created_at DESC, id DESC
        """).fetchall()

    return [
        {
            "id": row["id"],
            "customer": row["customer"],
            "item": row["item"],
            "amount": row["amount_paise"] / 100,
            "status": row["payment_status"],
        }
        for row in rows
    ]
