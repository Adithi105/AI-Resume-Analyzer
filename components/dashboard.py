import streamlit as st
from typing import Dict, Any

def render_candidate_dashboard(data: Dict[str, Any]):
    """
    Renders top candidate information metrics and ATS Score status card.
    """
    st.subheader("👤 Candidate Overview")
    
    # 4 Metric Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👤 Candidate Name", data.get("Name", "Not Provided"))

    with col2:
        st.metric("📧 Email Address", data.get("Email", "Not Provided"))

    with col3:
        st.metric("📞 Phone Number", data.get("Phone", "Not Provided"))

    ats_score = data.get("ATS_Score", 0)
    with col4:
        st.metric("⭐ Overall ATS Score", f"{ats_score} / 100")

    st.markdown("<br>", unsafe_allow_html=True)

    # ATS Score Status Badge & Progress Bar Container
    with st.container():
        st.markdown("### 📊 ATS Readiness Status")
        
        progress_val = max(0, min(100, ats_score)) / 100.0
        st.progress(progress_val)

        if ats_score >= 80:
            st.success("🎉 **EXCELLENT RESUME**: High ATS compliance! Strong formatting, relevant skills, and clear achievements detected.")
        elif ats_score >= 60:
            st.warning("🙂 **GOOD RESUME**: solid foundation, but key improvements in keywords, formatting, or project metrics can raise your score.")
        elif ats_score >= 40:
            st.info("⚠️ **AVERAGE RESUME**: Missing key sections or technical keywords required by modern automated screening systems.")
        else:
            st.error("🚨 **POOR RESUME**: Significant optimization needed. High risk of rejection by automated ATS filters.")
