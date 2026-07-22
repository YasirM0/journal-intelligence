"""
Export service.

Responsible for exporting recommendation results into different formats.

Works with the dictionary-based recommendation format returned by
services.recommender.JournalRecommender.recommend(), not the old
Recommendation dataclass.
"""

from typing import Iterable

import pandas as pd


def recommendations_to_rows(
    recommendations: Iterable[dict],
) -> list[dict]:
    """
    Convert recommendation dicts into flat dictionaries suitable for export.
    """

    rows = []

    for recommendation in recommendations:
        rows.append(
            {
                "Journal Name": recommendation["title"],
                "Score": recommendation["score"],
                "Publisher": recommendation["publisher"],
                "Country": recommendation["country"],
                "Languages": recommendation["languages"],
                "APC": "Free" if recommendation["is_free"] else recommendation["apc"],
                "APC Amount": recommendation["apc_amount"],
                "License": recommendation["license"],
                "Review Time (weeks)": recommendation["review_weeks"],
                "Website": recommendation["website"],
                "DOAJ URL": recommendation["doaj_url"],
                "Reasons": " | ".join(recommendation["reasons"]),
            }
        )

    return rows


def export_to_csv(
    recommendations: Iterable[dict],
) -> bytes:
    """
    Export recommendations as CSV data.
    """

    rows = recommendations_to_rows(recommendations)

    dataframe = pd.DataFrame(rows)

    return dataframe.to_csv(index=False).encode("utf-8")