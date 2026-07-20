import streamlit as st

st.set_page_config(
    page_title="Journal Intelligence",
    page_icon="📚",
    layout="wide",
)

st.title("Journal Intelligence")

st.markdown(
    """
    Welcome to the **Journal Intelligence** prototype.

    **Version:** 0.1 Alpha

    This application helps researchers discover journals that best match their manuscripts. The current version provides the initial application skeleton and interface foundation.
    """
)

st.sidebar.header("Journal Intelligence")

st.sidebar.info(
    "Use the navigation above to explore the application."
)