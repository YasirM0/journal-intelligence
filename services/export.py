"""
Export service.

Responsible for exporting recommendation results into different formats.
"""

from typing import Iterable

import pandas as pd

from models.recommendation import Recommendation


def recommendations_to_rows(
    recommendations: Iterable[Recommendation],
) -> list[dict]:
    """
    Convert Recommendation objects into dictionaries
    suitable for export.
    """

    rows = []

    for recommendation in recommendations:
        rows.append(
            {
                "Journal Name": recommendation.journal_name,
                "Recommendation Score": recommendation.recommendation_score,
                "Match Score": recommendation.match_score,
                "Indexing": recommendation.indexing,
                "Journal Rank": recommendation.journal_rank,
                "Publisher": recommendation.publisher,
                "Language": recommendation.language,
                "APC": recommendation.apc_display,
                "Submission URL": recommendation.submission_url,
            }
        )

    return rows


def export_to_csv(
    recommendations: Iterable[Recommendation],
) -> bytes:
    """
    Export recommendations as CSV data.
    """

    rows = recommendations_to_rows(recommendations)

    dataframe = pd.DataFrame(rows)

    return dataframe.to_csv(index=False).encode("utf-8")