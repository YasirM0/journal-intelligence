from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent

DB_PATH = ROOT / "data" / "journal_intelligence.db"
SCHEMA_PATH = ROOT / "data" / "schema.sql"


def main():
    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

    print(f"Database initialized: {DB_PATH}")


if __name__ == "__main__":
    main()