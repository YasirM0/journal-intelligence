from models.recommendation import Recommendation


def rank_journals(
    journals,
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
    list[Recommendation]
        Ranked journal recommendations.
    """

    results = journals.copy()

    # Start with textual similarity.
    results["final_score"] = results["match_score"]

    results = results.sort_values(
        by="final_score",
        ascending=False,
    )

    recommendations = []

    for _, row in results.iterrows():

        recommendations.append(
            Recommendation(
                journal_name=row["title"],
                publisher=row["publisher"],
                indexing=row["indexing"],
                journal_rank=row["quartile"],
                language=row["language"],
                submission_url=row["submission_url"],
                apc_display=f'{row["apc_currency"]} {row["apc"]}',
                apc_value=row["apc"],
                recommendation_score=row["final_score"],
                match_score=row["match_score"],
                reasons=[],
            )
        )

    return recommendations