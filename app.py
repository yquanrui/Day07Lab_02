import streamlit as st
from datetime import datetime

from config import GEMINI_MODEL
from database.db_manager import init_db, save_summary, get_summaries_by_category
from services.gemini_service import analyze_review_sentiment
from ui.views import render_archived_view, render_upload_view, render_analysis_result

MODEL_NAME = GEMINI_MODEL

# Initialize Database immediately
init_db()

# --- STREAMLIT PAGE LAYOUT ---
st.set_page_config(page_title="Review Analyst Pro", page_icon="📈", layout="wide")

# Initialize Session States to control UI navigation mapping
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "new_analysis"
if "selected_summary_id" not in st.session_state:
    st.session_state.selected_summary_id = None

# --- SIDEBAR COMPONENT ---
with st.sidebar:
    st.title("📁 Navigation & History")

    # Primary action to reset UI to standard uploader
    if st.button("➕ Analyze New Reviews", use_container_width=True, type="primary"):
        st.session_state.view_mode = "new_analysis"
        st.session_state.selected_summary_id = None
        st.rerun()

    st.divider()
    st.subheader("📜 Filter Past Summaries")

    # Category expander folders
    categories = {
        "🟢 Good (8-10)": "Good",
        "🟡 Average (4-7)": "Average",
        "🔴 Bad (0-3)": "Bad"
    }

    for label, db_category in categories.items():
        with st.expander(label):
            records = get_summaries_by_category(db_category)
            if not records:
                st.caption("No historical records found.")
            for rec_id, filename, timestamp in records:
                # Format time string for cleaner UI listings
                time_str = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f").strftime("%b %d, %H:%M")
                btn_label = f"📄 {filename} ({time_str})"

                # If a user clicks a historical record button, switch the view state
                if st.button(btn_label, key=f"rec_{rec_id}", use_container_width=True):
                    st.session_state.view_mode = "view_past"
                    st.session_state.selected_summary_id = rec_id
                    st.rerun()

# --- MAIN CONTROLLER ARENA ---

# MODE 1: View Past Record History
if st.session_state.view_mode == "view_past" and st.session_state.selected_summary_id is not None:
    render_archived_view(st.session_state.selected_summary_id)

# MODE 2: Run Fresh Analysis Uploader
else:
    upload_result = render_upload_view(MODEL_NAME)

    if upload_result is not None:
        filename, review_text = upload_result

        with st.spinner("Gemini is interpreting text blocks and mapping score parameters..."):
            try:
                clean_summary, rating, category = analyze_review_sentiment(review_text)
                save_summary(filename, clean_summary, rating, category)
                render_analysis_result(category, rating, clean_summary)
            except Exception as api_err:
                st.error(f"❌ Cloud API Request Interrupted: {api_err}")