def rank_journals(
    journals,
    preferred_indexing=None,
    preferred_language=None,
):
    """
    Rank journals after textual matching.

    The matching service determines how similar a journal is to the
    manuscript. This service then adjusts that score according to the
    user's publication preferences.

    Parameters
    ----------
    journals : pandas.DataFrame
        Journals returned from the matching engine.

    preferred_indexing : list[str] | None
        Preferred indexing systems.

    preferred_language : str | None
        Preferred publication language.

    Returns
    -------
    pandas.DataFrame
        Journals sorted by recommendation score.
    """

    results = journals.copy()

    # Start with textual similarity.
    results["final_score"] = results["match_score"]

    # Bonus for preferred indexing.
    if preferred_indexing:

        results.loc[
            results["indexing"].isin(preferred_indexing),
            "final_score",
        ] += 5

    # Bonus for preferred language.
    if preferred_language:

        results.loc[
            results["language"] == preferred_language,
            "final_score",
        ] += 3

    return results.sort_values(
        by="final_score",
        ascending=False,
    )