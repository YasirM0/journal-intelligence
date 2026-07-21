import streamlit as st

from utils.database import load_journals
from services.matching import match_journals
from services.ranking import rank_journals
from services.filtering import filter_journals
from services.export import export_to_csv
from datetime import datetime

if "search" not in st.session_state:
    st.session_state.search = None

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

    # Convert UI selections
    ranking_indexing = preferred_indexing or []
    ranking_language = (
        None if preferred_language == "Any"
        else preferred_language
    )

    results = filter_journals(
        journals=results,
        indexing=ranking_indexing,
        language=ranking_language,
    )
    
    results = rank_journals(
        journals=results,
    )

    # Show only the best recommendations.
    results = results[:10]
    st.session_state.search = {
        "results": results,
        "strategy": recommendation_strategy,
        "filters": {
            "indexing": preferred_indexing,
            "language": preferred_language,
            "budget": publication_budget,
        },
    }

    if not results:
        st.info(
            """
    ### No journals matched your current filters.

    Try one or more of the following:

    - Select additional indexing systems.
    - Choose **Any** as the preferred language.
    - Broaden your manuscript title, abstract, or keywords.
    """
        )
        st.stop()

# ==========================================================
# Recommendation Results
# ==========================================================

search = st.session_state.search

if search:

    results = search["results"]
    strategy = search["strategy"]

    st.success(
        f"Showing the top {len(results)} recommended journals."
    )

    if st.button("🗑️ Clear Search"):
        st.session_state.search = None
        st.rerun()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    strategy_slug = strategy.split(" ", 1)[1]
    strategy_slug = (
        strategy_slug
        .replace(" (Recommended)", "")
        .replace(" ", "_")
        .lower()
    )

    filename = (
        f"ji_{strategy_slug}_{timestamp}.csv"
    )

    csv_data = export_to_csv(results)

    st.download_button(
        label="📥 Download Recommendations (CSV)",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
    )
    
    st.caption(
        "🔒 Search results are stored only for this browser session "
        "and are never saved permanently."
    )

    for recommendation in results:

        with st.container(border=True):

            st.subheader(recommendation.journal_name)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Recommendation Score",
                    f"{recommendation.recommendation_score:.1f}",
                )

            with col2:
                st.write(
                    f"**Indexing:** {recommendation.indexing} ({recommendation.journal_rank})"
                )

            with col3:
                st.write(f"**Language:** {recommendation.language}")

            st.write(f"**APC:** {recommendation.apc_display}")
            st.write(f"**Publisher:** {recommendation.publisher}")

            st.link_button(
                "Visit Journal",
                recommendation.submission_url,
            )