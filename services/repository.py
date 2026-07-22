import sqlite3
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "journal_intelligence.db"


def get_connection():
    """
    Create a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)


def get_all_journals():
    """Retrieve all journals."""
    conn = get_connection()

    query = """
    SELECT *
    FROM journals
    """

    journals = pd.read_sql_query(query, conn)

    conn.close()

    return journals


def count_journals():
    """
    Return the number of journals stored in the database.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM journals
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def insert_journals(df):
    """Insert journals into the database."""

    conn = get_connection()

    df.to_sql(
        "journals",
        conn,
        if_exists="append",
        index=False,
    )

    conn.commit()
    conn.close()