import sqlite3
from datetime import datetime, date

from config import DB_FILE


def get_connection():

    conn = sqlite3.connect(
        DB_FILE,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            status TEXT NOT NULL DEFAULT 'PENDING',

            attempts INTEGER NOT NULL DEFAULT 0,

            last_error TEXT,

            sent_at TEXT,

            created_at TEXT NOT NULL
        )
    """)

    conn.commit()

    return conn


def add_contact(conn, name, email):

    try:

        conn.execute("""
            INSERT OR IGNORE INTO contacts
            (
                name,
                email,
                status,
                attempts,
                created_at
            )
            VALUES (?, ?, 'PENDING', 0, ?)
        """, (
            name,
            email,
            datetime.now().isoformat()
        ))

        conn.commit()

    except Exception as e:

        print(
            f"Database error for {email}: {e}"
        )


def get_pending_contacts(conn, limit):

    cursor = conn.execute("""
        SELECT
            id,
            name,
            email,
            status,
            attempts
        FROM contacts

        WHERE status IN ('PENDING', 'FAILED')

        AND attempts < 3

        ORDER BY id

        LIMIT ?
    """, (limit,))

    return cursor.fetchall()


def mark_sent(conn, contact_id):

    conn.execute("""
        UPDATE contacts

        SET
            status = 'SENT',
            sent_at = ?,
            last_error = NULL

        WHERE id = ?
    """, (
        datetime.now().isoformat(),
        contact_id
    ))

    conn.commit()


def mark_failed(conn, contact_id, error):

    conn.execute("""
        UPDATE contacts

        SET
            status = 'FAILED',
            attempts = attempts + 1,
            last_error = ?

        WHERE id = ?
    """, (
        str(error),
        contact_id
    ))

    conn.commit()


def get_today_sent_count(conn):

    today = date.today().isoformat()

    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM contacts
        WHERE status = 'SENT'
        AND sent_at LIKE ?
    """, (
        today + "%",
    ))

    return cursor.fetchone()[0]


def get_statistics(conn):

    cursor = conn.execute("""
        SELECT
            status,
            COUNT(*) AS count

        FROM contacts

        GROUP BY status
    """)

    return cursor.fetchall()