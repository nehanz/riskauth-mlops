import sqlite3
from datetime import datetime

conn = sqlite3.connect("events.db", check_same_thread=False)

conn.execute("""
CREATE TABLE IF NOT EXISTS auth_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    tenant_id TEXT,
    ip TEXT,
    device TEXT,
    login_time TEXT,
    risk_score REAL,
    decision TEXT,
    created_at TEXT
)
""")

def save_event(event: dict, risk_score: float, decision: str):
    conn.execute(
        """
        INSERT INTO auth_events
        (
            user_id, tenant_id, ip, device,
            login_time, risk_score, decision, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event["user_id"],
            event["tenant_id"],
            event["ip"],
            event["device"],
            event["login_time"].isoformat(),
            risk_score,
            decision,
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
