import sqlite3
from pathlib import Path
from dataclasses import asdict

import pandas as pd

from models.journal import Journal

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "journal_intelligence.db"


def get_connection():
    """
    Create a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)


def _rows_to_journals(dataframe):
    """
    Convert a pandas DataFrame into Journal objects.
    """

    return [
        Journal.from_row(row)
        for _, row in dataframe.iterrows()
    ]


def get_all_journals():
    """Retrieve all journals."""

    conn = get_connection()

    query = """
    SELECT *
    FROM journals
    """

    dataframe = pd.read_sql_query(query, conn)

    conn.close()

    return _rows_to_journals(dataframe)


def search_by_title(title):
    """Search journals by title."""

    conn = get_connection()

    query = """
    SELECT *
    FROM journals
    WHERE title LIKE ?
    """

    dataframe = pd.read_sql_query(
        query,
        conn,
        params=[f"%{title}%"]
    )

    conn.close()

    return _rows_to_journals(dataframe)


def search_journals(**filters):
    """Search journals using any combination of filters."""

    conn = get_connection()

    query = "SELECT * FROM journals"

    conditions = []
    params = []

    for column, value in filters.items():
        conditions.append(f"{column} LIKE ?")
        params.append(f"%{value}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    dataframe = pd.read_sql_query(
        query,
        conn,
        params=params
    )

    conn.close()

    return _rows_to_journals(dataframe)


def search_by_keywords(keywords):
    """
    Search journals matching any keyword in the title,
    subjects, or keywords fields.
    """

    # Remove empty keywords
    keywords = [
        keyword.strip()
        for keyword in keywords
        if keyword.strip()
    ]

    # If no keywords were provided, return all journals
    if not keywords:
        return get_all_journals()

    conn = get_connection()

    conditions = []
    params = []

    for keyword in keywords:

        conditions.extend([
            "title LIKE ?",
            "subjects LIKE ?",
            "keywords LIKE ?",
        ])

        params.extend([
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ])

    query = f"""
    SELECT DISTINCT *
    FROM journals
    WHERE {" OR ".join(conditions)}
    """

    dataframe = pd.read_sql_query(
        query,
        conn,
        params=params,
    )

    conn.close()

    return _rows_to_journals(dataframe)


def search_candidates(keywords, language=None, free_only=False):
    """
    Search journals matching any keyword in the title, subjects, or
    keywords fields, optionally narrowed by language and/or free-only.

    language:
        Substring match against the `languages` column
        (e.g. "English", "Indonesian").

    free_only:
        If True, only return journals with no publication fee (apc = "No").

    Note: budget (max APC) filtering is NOT done here. The `apc_amount`
    column is free text (e.g. "40 USD", "40 USD; 450000 IDR") rather than
    a clean number, so it can't be reliably compared in SQL. Budget
    filtering happens in Python, in the recommender, after parsing each
    value.
    """

    keywords = [
        keyword.strip()
        for keyword in keywords
        if keyword.strip()
    ]

    conn = get_connection()

    conditions = []
    params = []

    if keywords:
        keyword_conditions = []
        for keyword in keywords:
            keyword_conditions.append(
                "(title LIKE ? OR subjects LIKE ? OR keywords LIKE ?)"
            )
            params.extend([f"%{keyword}%"] * 3)
        conditions.append("(" + " OR ".join(keyword_conditions) + ")")

    if language:
        conditions.append("languages LIKE ?")
        params.append(f"%{language}%")

    if free_only:
        conditions.append("apc = 'No'")

    query = "SELECT DISTINCT * FROM journals"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    dataframe = pd.read_sql_query(query, conn, params=params)

    conn.close()

    return _rows_to_journals(dataframe)


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


def insert_journals(journals):
    """Insert Journal objects into the database."""

    conn = get_connection()

    rows = [asdict(journal) for journal in journals]

    pd.DataFrame(rows).to_sql(
        "journals",
        conn,
        if_exists="append",
        index=False,
    )

    conn.commit()
    conn.close()