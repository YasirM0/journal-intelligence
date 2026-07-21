import streamlit as st

from utils.database import load_journals
from services.matching import match_journals
from services.ranking import rank_journals


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Submission Search",
    page_icon="🔍",
)


# ==========================================================
# Load Journal Dataset
# ==========================================================
# The dataset is loaded once when the page starts.
# Later this can be cached using @st.cache_data.

journals = load_journals()


# Developer preview (temporary)
with st.expander("Developer Preview"):
    st.success(f"Loaded {len(journals)} journals.")
    st.dataframe(
        journals,
        width="stretch",
        hide_index=True,
    )


# ==========================================================
# Page Header
# ==========================================================

st.title("🔍 Journal Search")

st.write(
    "Upload your completed manuscript or enter its information manually "
    "to discover journals that best match your research."
)

st.divider()


# ==========================================================
# Upload Manuscript (Future Feature)
# ==========================================================

st.subheader("📎 Upload Manuscript (Recommended)")

st.write(
    "If you already have a completed manuscript, you will soon be able "
    "to upload it and automatically extract the title, abstract, and keywords."
)

st.file_uploader(
    "Upload PDF or DOCX",
    type=["pdf", "docx"],
    disabled=True,
)

st.caption(
    "🚧 Automatic manuscript extraction will be available in a future version."
)

st.divider()

st.markdown(
    "<div style='text-align:center; font-weight:bold; color:gray;'>OR</div>",
    unsafe_allow_html=True,
)

st.divider()


# ==========================================================
# Manual Manuscript Entry
# ==========================================================

st.subheader("📄 Enter Manuscript Information")

title = st.text_input(
    "Paper Title *",
    placeholder="Enter your manuscript title...",
)

abstract = st.text_area(
    "Abstract *",
    placeholder="Paste your manuscript abstract here...",
    height=220,
    help="Your abstract is the primary source used to identify suitable journals.",
)

keywords = st.text_input(
    "Keywords (Optional)",
    placeholder="digital governance, e-government, Indonesia",
    help="Separate keywords using commas (,) or semicolons (;).",
)

st.divider()


# ==========================================================
# Publication Preferences
# ==========================================================

st.caption(
    "Customize how Journal Intelligence recommends journals for your manuscript."
)

with st.expander("⚙️ Publication Preferences", expanded=False):

    # ------------------------------------------------------
    # Recommendation Strategy
    # Determines HOW journals are ranked after matching.
    # ------------------------------------------------------

    recommendation_strategy = st.selectbox(
        "Recommendation Strategy",
        [
            "⚖️ Balanced (Recommended)",
            "🎯 Best Match",
            "💰 Lowest APC",
            "🏆 Highest Prestige",
            "⚡ Fast Publication (Coming Soon)",
            "🌱 Beginner Friendly (Coming Soon)",
        ],
        help=(
            "Choose what Journal Intelligence should prioritize when "
            "ranking journals."
        ),
    )

    st.divider()

    # ------------------------------------------------------
    # Filters
    # These determine WHICH journals are eligible.
    # ------------------------------------------------------

    st.markdown("#### Filters")

    col1, col2 = st.columns(2)

    with col1:

        preferred_indexing = st.multiselect(
            "Preferred Indexing",
            [
                "Scopus",
                "SINTA",
                "DOAJ",
                "Web of Science",
                "Google Scholar",
            ],
            default=["Scopus", "SINTA"],
            help="Only prioritize journals from the selected indexing systems.",
        )

    with col2:

        preferred_language = st.selectbox(
            "Preferred Language",
            [
                "Any",
                "English",
                "Indonesian",
            ],
        )

    publication_budget = st.selectbox(
        "Publication Budget",
        [
            "Any",
            "Free (No APC)",
            "Low APC (< $100)",
            "Medium APC ($100–300)",
            "High APC (> $300)",
        ],
        help="Maximum publication fee you are willing to pay.",
    )

st.divider()


# ==========================================================
# Journal Recommendation
# ==========================================================

if st.button(
    "🔍 Find Best Matching Journals",
    width="stretch",
):

    # ------------------------------------------------------
    # Validate required fields
    # ------------------------------------------------------

    if not title or not abstract:
        st.warning("Please enter both a title and an abstract.")
        st.stop()

    # ------------------------------------------------------
    # Step 1
    # Find journals that are textually similar to the manuscript.
    # ------------------------------------------------------

    results = match_journals(
        title=title,
        abstract=abstract,
        keywords=keywords,
        journals=journals,
    )

    # Remove journals with zero similarity
    results = results[results["match_score"] > 0]

    # Convert "Any" into None so the ranking service ignores it.
    ranking_indexing = preferred_indexing or []
    ranking_language = None if preferred_language == "Any" else preferred_language


    # ------------------------------------------------------
    # Step 2
    # Apply publication preferences to create the final ranking.
    # ------------------------------------------------------

    results = rank_journals(
        journals=results,
        preferred_indexing=ranking_indexing,
        preferred_language=ranking_language,
    )

    # Show only the best recommendations.
    results = results.head(10)

    st.success(
        f"Showing the top {len(results)} recommended journals."
    )

    # ------------------------------------------------------
    # Prepare results for display.
    # ------------------------------------------------------

    display_results = results[
        [
            "journal_name",
            "final_score",
            "indexing",
            "journal_rank",
            "apc_amount",
        ]
    ].rename(
        columns={
            "journal_name": "Journal",
            "final_score": "Recommendation Score",
            "indexing": "Indexing",
            "journal_rank": "Rank",
            "apc_amount": "APC",
        }
    )

    st.dataframe(
        display_results,
        width="stretch",
        hide_index=True,
    )