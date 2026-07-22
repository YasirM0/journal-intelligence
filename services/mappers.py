from models.journal import Journal


def row_to_journal(row):

    return Journal(
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