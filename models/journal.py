"""
Journal domain model.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Journal:
    """
    Internal representation of a journal.

    All importers convert external data into this model before
    it is validated and stored in the database.
    """

    title: str

    publisher: str | None = None
    country: str | None = None

    website: str | None = None
    doaj_url: str |None = None

    issn_print: str | None = None
    issn_online: str | None = None

    subjects: str | None = None
    keywords: str | None = None
    languages: str | None = None

    apc: str | None = None
    apc_amount: str | None = None
    waiver_policy: str | None = None

    review_process: str | None = None
    review_weeks: int | None = None

    license: str | None = None

    article_count: int | None = None

    source: str | None = None

    @classmethod
    def from_row(cls, row):
        """
        Create a Journal from a database row.
        """

        return cls(
            title=row["title"],
            publisher=row["publisher"],
            country=row["country"],
            website=row["website"],
            doaj_url=row["doaj_url"],
            issn_print=row["issn_print"],
            issn_online=row["issn_online"],
            subjects=row["subjects"],
            keywords=row["keywords"],
            languages=row["languages"],
            apc=row["apc"],
            apc_amount=row["apc_amount"],
            waiver_policy=row["waiver_policy"],
            review_process=row["review_process"],
            review_weeks=row["review_weeks"],
            license=row["license"],
            article_count=row["article_count"],
            source=row["source"],
        )