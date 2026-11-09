import sqlite3
from contextlib import contextmanager
from app.core.config import DATABASE_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, price_paise INTEGER NOT NULL CHECK(price_paise >= 0), stock INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY, customer_email TEXT NOT NULL, status TEXT NOT NULL, total_paise INTEGER NOT NULL, created_at TEXT NOT NULL, due_at TEXT, environment TEXT NOT NULL DEFAULT 'sandbox'
);
CREATE TABLE IF NOT EXISTS payments (
  id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL UNIQUE, paypal_order_id TEXT UNIQUE, capture_id TEXT UNIQUE, status TEXT NOT NULL, amount_paise INTEGER NOT NULL, currency TEXT NOT NULL DEFAULT 'INR', created_at TEXT NOT NULL,
  FOREIGN KEY(order_id) REFERENCES orders(id)
);
CREATE TABLE IF NOT EXISTS webhook_events (
  event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, processed_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_logs (
  id INTEGER PRIMARY KEY, actor TEXT NOT NULL, action TEXT NOT NULL, created_at TEXT NOT NULL
);
"""


@contextmanager
def connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with connection() as conn:
        conn.executescript(SCHEMA)
        count = conn.execute("SELECT count(*) FROM orders").fetchone()[0]
        if count:
            return
        seed(conn)


def seed(conn: sqlite3.Connection) -> None:
    products = [("Artisan coffee beans", 89900, 24), ("Ceramic pour-over kit", 149900, 11), ("Monthly coffee subscription", 129900, 50)]
    conn.executemany("INSERT INTO products(name, price_paise, stock) VALUES (?, ?, ?)", products)
    orders = [
        ("maya@example.test", "PAID", 89900, "2026-11-02T07:30:00Z", None),
        ("arun@example.test", "PAID", 149900, "2026-11-01T12:20:00Z", None),
        ("lee@example.test", "PAID", 129900, "2026-10-30T09:05:00Z", None),
        ("nina@example.test", "PENDING_PAYMENT", 89900, "2026-10-29T15:40:00Z", "2026-10-31T15:40:00Z"),
        ("sam@example.test", "PAYMENT_FAILED", 149900, "2026-10-28T11:15:00Z", "2026-10-30T11:15:00Z"),
        ("ravi@example.test", "REFUNDED", 129900, "2026-10-27T10:00:00Z", None),
        ("dara@example.test", "PAID", 89900, "2026-10-24T16:30:00Z", None),
        ("zoe@example.test", "PAID", 149900, "2026-10-22T08:45:00Z", None),
        ("ivy@example.test", "PAID", 129900, "2026-10-19T13:10:00Z", None),
    ]
    conn.executemany("INSERT INTO orders(customer_email,status,total_paise,created_at,due_at) VALUES(?,?,?,?,?)", orders)
    payments = [
        (1, "PAYPAL-DEMO-101", "CAP-101", "CAPTURED", 89900, "2026-11-02T07:32:00Z"),
        (2, "PAYPAL-DEMO-102", "CAP-102", "CAPTURED", 149900, "2026-11-01T12:22:00Z"),
        (3, "PAYPAL-DEMO-103", "CAP-103", "CAPTURED", 129900, "2026-10-30T09:08:00Z"),
        (4, "PAYPAL-DEMO-104", None, "PENDING", 89900, "2026-10-29T15:41:00Z"),
        (5, "PAYPAL-DEMO-105", None, "FAILED", 149900, "2026-10-28T11:17:00Z"),
        (6, "PAYPAL-DEMO-106", "CAP-106", "REFUNDED", 129900, "2026-10-27T10:04:00Z"),
        (7, "PAYPAL-DEMO-107", "CAP-107", "CAPTURED", 89900, "2026-10-24T16:32:00Z"),
        (8, "PAYPAL-DEMO-108", "CAP-108", "CAPTURED", 149900, "2026-10-22T08:47:00Z"),
        (9, "PAYPAL-DEMO-109", "CAP-109", "CAPTURED", 129900, "2026-10-19T13:12:00Z"),
    ]
    conn.executemany("INSERT INTO payments(order_id,paypal_order_id,capture_id,status,amount_paise,created_at) VALUES(?,?,?,?,?,?)", payments)
