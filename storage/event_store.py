import sqlite3
from datetime import datetime

_conn = None


def get_connection(db_path: str = "events.db") -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(db_path, check_same_thread=False)
        _init_tables(_conn)
    return _conn


def _init_tables(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS auth_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            tenant_id TEXT,
            ip_address TEXT,
            country TEXT,
            city TEXT,
            latitude REAL,
            longitude REAL,
            asn TEXT,
            user_agent TEXT,
            device_type TEXT,
            rtt REAL,
            login_timestamp TEXT,
            login_success INTEGER,
            risk_score REAL,
            decision TEXT,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_baselines (
            user_id TEXT PRIMARY KEY,
            avg_login_hour REAL DEFAULT 12.0,
            avg_rtt REAL DEFAULT 50.0,
            known_countries TEXT DEFAULT '[]',
            known_cities TEXT DEFAULT '[]',
            known_asns TEXT DEFAULT '[]',
            known_devices TEXT DEFAULT '[]',
            success_ratio_7d REAL DEFAULT 1.0,
            account_age_days REAL DEFAULT 0.0,
            total_logins INTEGER DEFAULT 0,
            failed_logins_24h INTEGER DEFAULT 0,
            login_attempt_rate_1h REAL DEFAULT 0.0,
            last_login_timestamp TEXT,
            last_latitude REAL DEFAULT 0.0,
            last_longitude REAL DEFAULT 0.0,
            country_freq TEXT DEFAULT '{}',
            asn_freq TEXT DEFAULT '{}',
            device_freq TEXT DEFAULT '{}',
            first_login_timestamp TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()


def save_event(event: dict, risk_score: float, decision: str):
    conn = get_connection()
    ts = event.get("login_timestamp")
    if hasattr(ts, "isoformat"):
        ts = ts.isoformat()

    conn.execute(
        """
        INSERT INTO auth_events (
            user_id, tenant_id, ip_address, country, city,
            latitude, longitude, asn, user_agent, device_type,
            rtt, login_timestamp, login_success,
            risk_score, decision, created_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            event.get("user_id"),
            event.get("tenant_id"),
            event.get("ip_address"),
            event.get("country", "Unknown"),
            event.get("city", "Unknown"),
            event.get("latitude", 0.0),
            event.get("longitude", 0.0),
            event.get("asn", "Unknown"),
            event.get("user_agent", "Unknown"),
            event.get("device_type", "desktop"),
            event.get("rtt", 0.0),
            ts,
            1 if event.get("login_success", True) else 0,
            risk_score,
            decision,
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
