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

st.sidebar.header("Navigation")

navigation_items = [
    "Home",
    "Search",
    "About",
    "Settings",
]

for item in navigation_items:
    st.sidebar.write(f"• {item}")