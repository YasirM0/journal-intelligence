from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_journals(title, abstract, keywords, journals):
    """
    Compare a manuscript against all journals and return
    the journals sorted by relevance.
    """

    # Combine the user's input into one piece of text
    user_text = f"{title} {abstract} {keywords}"

    # Combine each journal's searchable text
    journal_texts = (
        journals["scope"].fillna("")
        + " "
        + journals["keywords"].fillna("")
    )

    # Build a list containing the user's text followed by every journal
    documents = [user_text] + journal_texts.tolist()

    # Convert text into numerical vectors
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compare the user's text against every journal
    similarities = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    ).flatten()

    # Copy the dataframe so we don't modify the original
    results = journals.copy()

    # Convert similarity to a percentage
    results["match_score"] = (similarities * 100).round(2)

    # Return highest scores first
    return results.sort_values(
        by="match_score",
        ascending=False
    )