import streamlit as st

st.set_page_config(
    page_title="Journal Intelligence",
    page_icon="📚",
)

st.title("📚 Journal Intelligence")

st.write(
    "Find the right journal at every stage of your research journey."
)

st.divider()

st.header("How would you like to begin?")

st.write(
    "Choose the workflow that best matches your current stage of research."
)

col1, col2 = st.columns(2)

# ==========================================================
# Planning Workflow
# ==========================================================

with col1:

    st.subheader("🌱 Planning")

    st.write(
        "I'm still planning or writing my manuscript and want to identify "
        "suitable journals before I start writing."
    )

    if st.button(
        "🌱 Start Planning",
        use_container_width=True,
    ):
        st.warning(
            "🚧 The Planning Workflow is currently under development."
        )

        st.markdown(
            """
### Planned Features

- ✅ Discover suitable journals before writing
- ✅ Download journal templates
- ✅ View author guidelines
- ✅ Explore journal scope and aims
- ✅ Receive journal-specific writing recommendations

*These features will be implemented in future versions.*
"""
        )

# ==========================================================
# Submission Workflow
# ==========================================================

with col2:

    st.subheader("🚀 Submission")

    st.write(
        "I already have a completed manuscript and want to find the most "
        "suitable journal for publication."
    )

    if st.button(
        "🚀 Submission Search",
        use_container_width=True,
    ):
        st.switch_page("pages/1_Submission_Search.py")

st.divider()

st.caption(
    "Journal Intelligence is designed to support researchers throughout the "
    "publication journey—from selecting a target journal before writing to "
    "identifying the best publication venue for a completed manuscript."
)

st.markdown(
    "<p style='text-align:center; color:gray;'><em>Supporting researchers from idea to publication.</em></p>",
    unsafe_allow_html=True,
)