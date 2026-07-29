"""
Admin Panel Module — System user management, database logs, API tester, and environment controls.
"""
import streamlit as st
from database.db import get_all_users, get_system_logs, create_user
from helpers.auth import get_user_role


def render_admin_panel():
    """Renders System Admin Control Panel."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #EC4899, #F43F5E);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            👑 System Admin Control Panel
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Manage user accounts, inspect system event logs, monitor database health, and view REST API documentation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    role = get_user_role()
    if role != "Admin":
        st.warning("⚠️ Admin privileges required to access full system controls. You are currently viewing in preview mode.")

    tab_users, tab_logs, tab_api = st.tabs(["👥 User Management", "📜 System Event Logs", "🔌 REST API Documentation"])

    with tab_users:
        st.markdown("### Registered System Accounts")
        users = get_all_users()

        for u in users:
            r_color = "#EC4899" if u['role'] == "Admin" else "#3B82F6" if u['role'] == "Recruiter" else "#10B981"
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                        border-radius: 12px; padding: 12px 18px; margin-bottom: 8px;
                        display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #F8FAFC;">{u['name']}</strong> ({u['email']}) — <em>{u['company']}</em>
                </div>
                <div style="background: {r_color}22; color: {r_color}; border: 1px solid {r_color}44;
                            padding: 2px 10px; border-radius: 10px; font-weight: 700; font-size: 0.8rem;">
                    {u['role']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_logs:
        st.markdown("### 📜 System Event Audit Trail")
        logs = get_system_logs()
        if not logs:
            st.info("No system events logged yet.")
        else:
            for log in logs:
                st.markdown(f"⏱️ `{log.get('created_at', '')[:19]}` | **{log.get('event_type')}** | User: `{log.get('user_email')}` | Details: {log.get('details')}")

    with tab_api:
        st.markdown("""
        ### 🔌 Enterprise REST API Documentation
        The Enterprise Recruitment Platform exposes RESTful HTTP endpoints for external integrations:

        - `GET /api/v1/health` — API status check
        - `GET /api/v1/candidates` — Fetch audited candidate database
        - `POST /api/v1/analyze` — Trigger automated AI resume audit via HTTP JSON payload
        - `GET /api/v1/interviews` — Retrieve scheduled candidate interview calendar

        Run server: `python -m api.server` (Serves on `http://localhost:8000`)
        """)
