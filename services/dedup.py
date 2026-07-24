"""
Journal deduplication / merge helpers.

Used by the import pipeline (scripts/build_database.py) to match
incoming rows from Scopus/WoS/SINTA against journals already in the
database, so each real-world journal ends up as ONE row, tagged with
every source it's confirmed in, instead of one row per source.

Match order: ISSN (print or online) first, then an EXACT normalized-title
match as a fallback. This is not fuzzy matching — two records for the
same journal with meaningfully different titles (e.g. one includes a
subtitle the other doesn't) will not be merged and will end up as
separate rows. That's a real limitation, not a bug; flagged in the
import summary as a validation warning so it can be checked by hand.
"""

import re


def normalize_title(title):
    if not title:
        return None
    normalized = str(title).lower()
    normalized = re.sub(r"[^a-z0-9\s]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized or None


class JournalIndex:
    """
    In-memory index of existing journals (by ISSN and normalized title),
    used to match incoming rows during import. Reflects whatever has
    already been committed to the `journals` table when it's built —
    rebuild it (or update it manually, see `add`) after writes.
    """

    def __init__(self, conn):
        self.by_issn = {}
        self.by_title = {}

        rows = conn.execute(
            "SELECT id, title, issn_print, issn_online FROM journals"
        ).fetchall()

        for journal_id, title, issn_print, issn_online in rows:
            if issn_print:
                self.by_issn.setdefault(issn_print, journal_id)
            if issn_online:
                self.by_issn.setdefault(issn_online, journal_id)
            normalized = normalize_title(title)
            if normalized:
                self.by_title.setdefault(normalized, journal_id)

    def find(self, issns, title):
        """Returns (journal_id, match_type) or (None, None)."""
        for issn in issns:
            if issn in self.by_issn:
                return self.by_issn[issn], "issn"

        normalized = normalize_title(title)
        if normalized and normalized in self.by_title:
            return self.by_title[normalized], "title"

        return None, None

    def add(self, journal_id, issns, title):
        """Register a newly created journal so later rows in the same
        import (or a later source) can match against it without a
        fresh DB round-trip."""
        for issn in issns:
            self.by_issn.setdefault(issn, journal_id)
        normalized = normalize_title(title)
        if normalized:
            self.by_title.setdefault(normalized, journal_id)
