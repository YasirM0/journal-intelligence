"""
Filtering service.

Determines which journals are eligible before ranking.
"""

def filter_journals(
    journals,
    indexing=None,
    language=None,
):
    """
    Filter journals according to user preferences.
    """

    results = journals.copy()

    if indexing:
        results = results[
            results["indexing"].isin(indexing)
        ]

    if language:
        results = results[
            results["language"] == language
        ]

    return results