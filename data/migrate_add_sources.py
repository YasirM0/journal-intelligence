"""
One-time, safe migration: adds a journal_sources table so a journal can
be tagged with multiple indexing sources (DOAJ, and later Scopus, SINTA,
Web of Science, etc.) instead of a single `source` text column.

Does NOT touch the existing `journals` table or its data. Safe to run
more than once (idempotent).
"""

import sqlite3

DB_PATH = "data/journal_intelligence.db"


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS journal_sources (
            journal_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            PRIMARY KEY (journal_id, source),
            FOREIGN KEY (journal_id) REFERENCES journals(id)
        )
    """)

    # Backfill from the existing single-value `source` column.
    # Today that means every journal gets a ('DOAJ',) row, because that's
    # genuinely the only source this dataset has ever come from.
    cur.execute("""
        INSERT OR IGNORE INTO journal_sources (journal_id, source)
        SELECT id, source FROM journals WHERE source IS NOT NULL
    """)

    conn.commit()

    count = cur.execute("SELECT COUNT(*) FROM journal_sources").fetchone()[0]
    by_source = cur.execute(
        "SELECT source, COUNT(*) FROM journal_sources GROUP BY source"
    ).fetchall()

    print(f"journal_sources ready: {count} rows total")
    for source, n in by_source:
        print(f"  {source}: {n}")

    conn.close()


if __name__ == "__main__":
    migrate()