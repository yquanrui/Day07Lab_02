import streamlit as st

from database.db_manager import get_summary_by_id


def render_archived_view(summary_id):
    """Renders a previously-saved analysis pulled from the database."""
    record = get_summary_by_id(summary_id)

    if not record:
        st.error("Could not retrieve the specified historical record.")
        return

    filename, summary, rating, category, created_at = record

    st.title(f"📜 Archived Summary: {filename}")
    st.caption(f"Analyzed on: {created_at} | Category Tier: **{category}**")
    st.markdown("---")

    col1, col2 = st.columns([1, 4])
    with col1:
        st.metric(label="Overall Rating", value=f"{rating} / 10")
    with col2:
        if category == "Good":
            st.success("🎯 Category Score: This batch reflects overall positive customer sentiment.")
        elif category == "Average":
            st.warning("⚖️ Category Score: This batch reflects mixed or average customer sentiment.")
        else:
            st.error("⚠️ Category Score: This batch reflects critical or negative customer sentiment.")

    st.markdown("### 📋 Core Synthesis Summary")
    st.markdown(summary)


def render_upload_view(model_name):
    """
    Renders the file-uploader + 'run analysis' button.
    Returns (filename, review_text) once the user has uploaded a file
    AND clicked the analyze button — otherwise returns None.
    """
    st.title("📊 Customer Review Analytics Engine")
    st.caption(f"Cloud Architecture Backend: **{model_name}**")
    st.markdown("---")

    st.markdown("""
    ### 📥 Processing Pipeline
    Upload a text file containing compilation feedback. The platform will evaluate metrics,
    generate structured takeaways, and catalog the entry into the database repository automatically.
    """)

    uploaded_file = st.file_uploader("Drop customer feedback .txt file here", type=["txt"])

    if uploaded_file is None:
        return None

    try:
        review_text = uploaded_file.read().decode("utf-8")
    except Exception as file_err:
        st.error(f"❌ Structural Read Error: {file_err}")
        return None

    with st.expander("📄 Review File Context Preview", expanded=False):
        st.text(review_text)

    st.markdown("---")

    if st.button("🚀 Execute Sentiment Analysis", use_container_width=True):
        return uploaded_file.name, review_text

    return None


def render_analysis_result(category, rating, clean_summary):
    """Renders the result of a freshly-run analysis."""
    st.success(f"✅ Processing Finalized! Saved under **{category}** classification category.")

    m_col, d_col = st.columns([1, 4])
    m_col.metric(label="Calculated Score", value=f"{rating} / 10")
    d_col.info(f"Database Router Pipeline assigned this to the **{category}** segment container.")

    st.markdown("### 📋 AI Generated Synthesis Review")
    st.markdown(clean_summary)