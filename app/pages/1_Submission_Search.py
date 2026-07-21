import streamlit as st

from utils.database import load_journals
from services.matching import match_journals

st.set_page_config(
    page_title="Submission Search",
    page_icon="🔍",
)

journals = load_journals()

with st.expander("Developer Preview"):
    st.success(f"Loaded {len(journals)} journals.")
    st.dataframe(journals, use_container_width=True, hide_index=True)

st.title("🔍 Journal Search")

st.write(
    "Upload your completed manuscript or enter its information manually "
    "to discover journals that best match your research."
)

st.divider()

# ==========================================================
# Upload Manuscript
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
# Manual Entry
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
    "Customize your search by specifying publication preferences."
)

with st.expander("⚙️ Publication Preferences", expanded=False):

    st.markdown("#### Journal Indexing")

    col1, col2 = st.columns(2)

    with col1:
        st.checkbox("Scopus", value=True)
        st.checkbox("SINTA", value=True)
        st.checkbox("DOAJ")

    with col2:
        st.checkbox("Web of Science")
        st.checkbox("Google Scholar")

    st.divider()

    st.markdown("#### Maximum APC")

    st.selectbox(
        "Publication Budget",
        [
            "Any",
            "Free (No APC)",
            "Budget",
            "Standard",
            "Premium",
        ],
        help=(
            "Budget ranges will automatically adapt to the selected "
            "journal indexing in a future version."
        ),
    )

    st.divider()

    st.markdown("#### Language")

    st.selectbox(
        "Preferred Language",
        [
            "Any",
            "English",
            "Indonesian",
        ],
    )

st.divider()

# ==========================================================
# Search
# ==========================================================

if st.button(
    "🔍 Find Best Matching Journals",
    use_container_width=True,
):

    if not title or not abstract:
        st.warning("Please enter both a title and an abstract.")
        st.stop()

    results = match_journals(
        title=title,
        abstract=abstract,
        keywords=keywords,
        journals=journals,
    )

    # Keep only relevant journals
    results = results[results["match_score"] > 0]

    # Show only the top 10 matches
    results = results.head(10)

    st.success(f"Showing the top {len(results)} matching journals.")

    display_results = results[
        [
            "journal_name",
            "match_score",
            "indexing",
            "journal_rank",
            "apc_amount",
        ]
    ].rename(
        columns={
            "journal_name": "Journal",
            "match_score": "Match (%)",
            "indexing": "Indexing",
            "journal_rank": "Rank",
            "apc_amount": "APC",
        }
    )

    st.dataframe(
        display_results,
        use_container_width=True,
        hide_index=True,
    )