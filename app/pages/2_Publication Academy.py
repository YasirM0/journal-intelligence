import streamlit as st

st.set_page_config(
    page_title="Publication Academy",
    page_icon="🎓",
)

st.title("🎓 Publication Academy")

st.write(
    "Learn the fundamentals of academic publishing and discover how to "
    "navigate the publication process with confidence."
)

st.divider()

st.info(
    "🚧 Publication Academy is currently under development. "
    "Educational content will be introduced gradually beginning in Version 0.3."
)

st.header("📖 Publishing Basics")

st.markdown("""
- What is an academic journal?
- Peer review
- Open Access
- Article Processing Charges (APC)
- Predatory journals
""")

st.header("📊 Journal Rankings")

st.markdown("""
- Scopus
- SINTA
- Web of Science
- DOAJ
- Journal Quartiles (Q1–Q4)
- Impact Factor
- CiteScore
""")

st.header("📝 Preparing Your Manuscript")

st.markdown("""
- Choosing the right journal
- Understanding journal scope
- Formatting your manuscript
- Keywords and abstracts
- Writing a cover letter
""")

st.header("🚀 After Submission")

st.markdown("""
- Editorial screening
- Peer review
- Revision process
- Acceptance and publication
""")

st.divider()

st.success(
    "Our goal is to help researchers understand the publication process—not just find journals."
)

st.caption(
    "Version 0.3 will introduce interactive lessons, contextual explanations, "
    "and beginner-friendly learning paths."
)