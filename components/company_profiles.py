"""
Company Profiles Module — Manage company directory, industry profiles, and active hiring requisitions.
"""
import streamlit as st
from database.db import get_all_companies, add_company


def render_company_profiles_section():
    """Renders Company Profiles & Job Requisitions UI."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #6366F1, #38BDF8);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🏢 Company Profiles & Job Requisitions Directory
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Target hiring companies, industry domain profiles, and active open job requisitions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    companies = get_all_companies()

    with st.expander("➕ Add New Company Profile", expanded=False):
        c_name = st.text_input("Company Name", key="comp_add_name")
        c_ind = st.text_input("Industry Domain", value="Cloud & Software", key="comp_add_ind")
        c_dom = st.text_input("Website Domain", placeholder="example.com", key="comp_add_dom")
        c_loc = st.text_input("Location / HQ", placeholder="San Francisco, CA", key="comp_add_loc")
        c_reqs = st.number_input("Open Job Requisitions Count", min_value=1, max_value=100, value=3, key="comp_add_reqs")

        if st.button("Save Company Profile", type="primary", use_container_width=True, key="btn_save_company"):
            if not c_name or not c_ind:
                st.error("Please enter Company Name and Industry.")
            else:
                ok = add_company(c_name, c_ind, c_dom, c_loc, c_reqs)
                if ok:
                    st.success(f"✅ Company profile '{c_name}' created!")
                    st.rerun()
                else:
                    st.error("Company profile with this name already exists.")

    st.markdown("### 🏢 Partner Companies Directory")

    for comp in companies:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 14px; padding: 16px; margin-bottom: 12px;
                    display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong style="font-size:1.15rem; color:#F8FAFC;">{comp.get('name')}</strong>
                <span style="color:#94A3B8; font-size:0.85rem; margin-left:8px;">({comp.get('domain', 'N/A')})</span>
                <div style="color:#CBD5E1; font-size:0.85rem; margin-top:4px;">
                    🏭 Industry: {comp.get('industry')} | 📍 Location: {comp.get('location')}
                </div>
            </div>
            <div style="background: rgba(99,102,241,0.15); color: #818CF8; border: 1px solid rgba(99,102,241,0.4);
                        padding: 6px 14px; border-radius: 12px; font-weight: 700; font-size: 0.88rem;">
                {comp.get('requisitions_count', 1)} Open Requisitions
            </div>
        </div>
        """, unsafe_allow_html=True)
