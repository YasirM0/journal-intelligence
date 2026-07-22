import streamlit as st

from services.recommender import JournalRecommender, STRATEGIES
from services.export import export_to_csv

st.set_page_config(
    page_title="Submission Search",
    page_icon="🔍",
)

st.title("🔍 Submission Search")

st.write(
    "Enter your manuscript information to receive journal recommendations."
)

# ==========================================================
# Upload Manuscript
# ==========================================================

with st.expander("📄 Upload manuscript (optional)"):

    uploaded_file = st.file_uploader(
        "Upload a PDF or DOCX file",
        type=["pdf", "docx"],
    )

    if uploaded_file is not None:
        st.info(
            "Automatic extraction of title/abstract/keywords from uploaded "
            "files isn't built yet — please fill in the fields below "
            "manually for now."
        )

# ==========================================================
# Manual Entry
# ==========================================================

title = st.text_input(
    "Paper Title",
)

abstract = st.text_area(
    "Abstract",
    height=200,
)

keywords = st.text_input(
    "Keywords (comma separated)",
    placeholder="digital governance, e-government, Indonesia",
)

st.divider()

# ==========================================================
# Publication Preferences
# ==========================================================

st.subheader("Publication Preferences")

pref_col1, pref_col2, pref_col3 = st.columns(3)

with pref_col1:
    # Real strategies first, plus roadmap items shown but marked "Coming soon"
    # rather than silently faked with made-up scores.
    strategy_options = STRATEGIES + [
        "Best Match (Coming soon)",
        "Highest Prestige (Coming soon)",
        "Beginner Friendly (Coming soon)",
    ]
    strategy = st.selectbox(
        "Recommendation Strategy",
        strategy_options,
        index=0,
        help=(
            "Best Match, Highest Prestige, and Beginner Friendly need data "
            "(semantic similarity, journal rank, acceptance rate) that "
            "isn't in the database yet."
        ),
    )

with pref_col2:
    language_choice = st.selectbox(
        "Preferred Language",
        ["Any", "English", "Indonesian"],
        index=0,
    )

with pref_col3:
    budget_choice = st.selectbox(
        "Publication Budget",
        ["Any", "Free", "<$100", "$100–300", ">$300"],
        index=0,
    )

with st.expander("ℹ️ About these filters"):
    st.caption(
        "Language filtering uses each journal's listed languages. "
        "Budget filtering uses each journal's listed APC — where a fee "
        "applies but no USD figure could be confirmed, that journal is "
        "left out of budget-limited searches rather than guessed at. "
        "Indexing filters (Scopus, SINTA, Web of Science) aren't available "
        "yet — this database is sourced from DOAJ, so all listed journals "
        "are DOAJ-indexed by definition, but other indexes aren't tracked."
    )

st.divider()

# ==========================================================
# Search
# ==========================================================

if st.button(
    "🔍 Find Journals",
    use_container_width=True,
):

    if not title:
        st.warning("Please enter a paper title.")
        st.stop()

    keyword_list = [
        k.strip()
        for k in keywords.replace(";", ",").split(",")
        if k.strip()
    ]

    language = None if language_choice == "Any" else language_choice

    free_only = budget_choice == "Free"
    min_budget = None
    max_budget = None
    if budget_choice == "<$100":
        max_budget = 99.99
    elif budget_choice == "$100–300":
        min_budget, max_budget = 100, 300
    elif budget_choice == ">$300":
        min_budget = 300

    resolved_strategy = strategy if strategy in STRATEGIES else "Balanced"
    if strategy not in STRATEGIES:
        st.info(f'"{strategy.split(" (")[0]}" isn\'t available yet — showing Balanced results instead.')

    recommender = JournalRecommender()

    results = recommender.recommend(
        title=title,
        keywords=keyword_list,
        abstract=abstract,
        language=language,
        free_only=free_only,
        min_budget=min_budget,
        max_budget=max_budget,
        strategy=resolved_strategy,
    )

    st.session_state.results = results


# ==========================================================
# Recommendation Results
# ==========================================================

if "results" in st.session_state:

    results = st.session_state.results

    st.success(f"Found {len(results)} journal recommendations.")

    if results:
        csv_bytes = export_to_csv(results)
        st.download_button(
            "⬇️ Export as CSV",
            data=csv_bytes,
            file_name="journal_recommendations.csv",
            mime="text/csv",
            use_container_width=True,
        )

    for journal in results:

        with st.container(border=True):

            st.subheader(journal["title"])

            info_col1, info_col2 = st.columns(2)

            with info_col1:
                st.write(f"**Publisher:** {journal['publisher']}")
                st.write(f"**Country:** {journal['country']}")
                st.write(f"**Language(s):** {journal['languages']}")

            with info_col2:
                apc_label = "Free" if journal["is_free"] else (
                    f"~${journal['apc_amount']:.0f}"
                    if journal["apc_amount"] is not None
                    else "Paid (amount not confirmed in USD)"
                )
                st.write(f"**APC:** {apc_label}")
                st.write(f"**License:** {journal['license'] or 'Not listed'}")
                if journal["review_weeks"] is not None:
                    st.write(f"**Typical review time:** ~{journal['review_weeks']} weeks")

            st.write(f"**Score:** {journal['score']}")

            if journal["website"]:
                st.link_button(
                    "Visit Journal",
                    journal["website"],
                )

            if journal["reasons"]:

                st.write("**Why this journal?**")

                for reason in journal["reasons"]:
                    st.write(f"- {reason}")