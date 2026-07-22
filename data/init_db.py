import sqlite3
import pandas as pd
from pathlib import Path
from services.repository import insert_journals

DATA_DIR = Path(__file__).parent
DB_PATH = DATA_DIR / "journal_intelligence.db"
SCHEMA_PATH = DATA_DIR / "schema.sql"
CSV_PATH = DATA_DIR / "journals.csv"


def initialize_database():
    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print(f"Database initialized at: {DB_PATH}")


def seed_database():
    """Populate the database from the CSV dataset."""

    df = pd.read_csv(CSV_PATH)

    # Map prototype CSV columns to database schema
    df = df.rename(columns={
        "journal_name": "title",
        "journal_rank": "quartile",
        "apc_amount": "apc",
        "scope": "discipline",
        "keywords": "match_keywords",
    })

    # Add columns that don't exist in the prototype CSV
    df["issn_print"] = None
    df["issn_online"] = None
    df["country"] = None
    df["subdiscipline"] = None
    df["open_access"] = None
    df["website"] = None
    df["last_updated"] = None

    # Reorder columns to match the database schema
    df = df[
        [
            "title",
            "publisher",
            "issn_print",
            "issn_online",
            "country",
            "language",
            "discipline",
            "subdiscipline",
            "indexing",
            "quartile",
            "apc",
            "apc_currency",
            "open_access",
            "website",
            "submission_url",
            "match_keywords",
            "last_updated",
        ]
    ]
    
    insert_journals(df)
    print(f"Imported {len(df)} journals.")


if __name__ == "__main__":
    initialize_database()
    seed_database()