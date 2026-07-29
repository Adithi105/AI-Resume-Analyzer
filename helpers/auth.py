"""
Authentication & Access Control Module — Handles role-based logins (Admin, Recruiter, Candidate),
session state authorization, and auth UI header/forms.
"""
import streamlit as st
from database.db import get_user_by_email, create_user, hash_password, log_system_event, init_db

# Initialize database tables on load
init_db()

_SESSION_USER = "auth_current_user"


def get_logged_in_user() -> dict:
    """Returns the currently authenticated user dict or None."""
    return st.session_state.get(_SESSION_USER)


def is_authenticated() -> bool:
    return _SESSION_USER in st.session_state and st.session_state[_SESSION_USER] is not None


def get_user_role() -> str:
    user = get_logged_in_user()
    return user.get("role", "Candidate") if user else "Guest"


def logout():
    """Logs out the current user."""
    user = get_logged_in_user()
    if user:
        log_system_event("USER_LOGOUT", user["email"], f"User {user['email']} logged out.")
    st.session_state.pop(_SESSION_USER, None)
    st.rerun()


def render_auth_header():
    """Renders the top authentication status bar & role switcher badge."""
    user = get_logged_in_user()

    if not user:
        # Default guest / quick login bar
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 12px; padding: 10px 16px; margin-bottom: 16px;
                    display: flex; justify-content: space-between; align-items: center;">
            <div style="color: #94A3B8; font-size: 0.88rem;">
                🔑 <strong>Authentication Status</strong>: Guest Mode (Full Feature Access Enabled)
            </div>
            <div>
                <span style="font-size:0.75rem; color:#64748B;">Demo Accounts: admin@recruimind.ai | recruiter@recruimind.ai</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        role = user.get("role", "Candidate")
        role_color = "#EC4899" if role == "Admin" else "#3B82F6" if role == "Recruiter" else "#10B981"
        role_icon = "👑" if role == "Admin" else "💼" if role == "Recruiter" else "👤"

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 12px; padding: 10px 16px; margin-bottom: 16px;
                        display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 1.3rem;">{role_icon}</div>
                <div>
                    <div style="font-weight: 700; color: #F8FAFC; font-size: 0.95rem;">
                        {user.get('name')} <span style="font-weight:400; color:#94A3B8;">({user.get('email')})</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #64748B;">
                        {user.get('company')}
                    </div>
                </div>
                <div style="margin-left: auto; background: {role_color}22; color: {role_color};
                            border: 1px solid {role_color}44; padding: 2px 10px; border-radius: 12px;
                            font-size: 0.75rem; font-weight: 700;">
                    {role.upper()} ROLE
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("🚪 Logout", key="btn_auth_logout", use_container_width=True):
                logout()


def render_auth_dialog():
    """Renders login and signup form tabs inside sidebar or main view."""
    st.sidebar.markdown("### 🔐 User Authentication")

    user = get_logged_in_user()
    if user:
        st.sidebar.success(f"Logged in as **{user['name']}** ({user['role']})")
        if st.sidebar.button("Log Out", key="sidebar_logout_btn"):
            logout()
        return

    auth_tab1, auth_tab2 = st.sidebar.tabs(["🔑 Login", "📝 Sign Up"])

    with auth_tab1:
        email_in = st.text_input("Email", placeholder="recruiter@recruimind.ai", key="login_email")
        pass_in = st.text_input("Password", type="password", key="login_password")

        if st.button("Log In", type="primary", use_container_width=True, key="btn_submit_login"):
            if not email_in or not pass_in:
                st.sidebar.error("Please fill email and password.")
            else:
                db_user = get_user_by_email(email_in)
                if db_user and db_user["password_hash"] == hash_password(pass_in):
                    st.session_state[_SESSION_USER] = db_user
                    log_system_event("USER_LOGIN", email_in, f"Successful login as {db_user['role']}")
                    st.sidebar.success(f"Welcome back, {db_user['name']}!")
                    st.rerun()
                else:
                    st.sidebar.error("Invalid email or password.")

        st.sidebar.caption("Demo: `admin@recruimind.ai` / `admin123` or `recruiter@recruimind.ai` / `recruiter123`")

    with auth_tab2:
        su_name = st.text_input("Full Name", key="signup_name")
        su_email = st.text_input("Email Address", key="signup_email")
        su_pass = st.text_input("Create Password", type="password", key="signup_pass")
        su_role = st.selectbox("Select Account Role", options=["Candidate", "Recruiter", "Admin"], key="signup_role")
        su_company = st.text_input("Company / Organization", value="Enterprise Tech", key="signup_company")

        if st.button("Create Account", use_container_width=True, key="btn_submit_signup"):
            if not su_name or not su_email or not su_pass:
                st.sidebar.error("Please fill all required fields.")
            else:
                ok = create_user(su_email, su_pass, su_name, su_role, su_company)
                if ok:
                    st.sidebar.success("Account created! Please log in.")
                    log_system_event("USER_SIGNUP", su_email, f"New user created: {su_role}")
                else:
                    st.sidebar.error("An account with this email already exists.")
