import sqlite3
from datetime import datetime

DB_NAME = "sentinelai.db"

# ---------------------------------------
# Create Database
# ---------------------------------------
def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_type TEXT,
            content TEXT,
            prediction TEXT,
            confidence REAL,
            risk TEXT,
            scanned_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------
# Save Scan
# ---------------------------------------
def save_scan(scan_type, content, prediction, confidence, risk):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scan_history
        (scan_type, content, prediction, confidence, risk, scanned_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        scan_type,
        content,
        prediction,
        confidence,
        risk,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ---------------------------------------
# Get All Scans
# ---------------------------------------
def get_scans():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM scan_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ---------------------------------------
# Dashboard Statistics
# ---------------------------------------
def get_total_scans():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_history")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_safe_scans():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM scan_history
        WHERE prediction='SAFE'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_phishing_scans():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM scan_history
        WHERE prediction='PHISHING'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ---------------------------------------
# Recent Activity
# ---------------------------------------
def get_recent_scans(limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            scan_type,
            content,
            prediction,
            confidence,
            risk,
            scanned_at
        FROM scan_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()

    conn.close()

    return rows