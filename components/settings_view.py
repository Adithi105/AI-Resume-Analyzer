"""
Settings View — AI Provider Configuration Page.

Allows users to:
  - Select provider (Ollama / OpenAI / Gemini / Claude)
  - Select a model from a dynamic per-provider list
  - Enter API keys securely (password masked)
  - Test connection
  - Save config to session state + optional .env file
"""
import streamlit as st
from helpers.config_manager import (
    load_config,
    save_config,
    get_current_provider_name,
    get_current_model,
    get_current_api_key,
)
from helpers.providers import PROVIDER_NAMES, PROVIDER_ICONS

# Provider metadata for display
PROVIDER_DESCRIPTIONS = {
    "Ollama": {
        "color": "#a78bfa",
        "badge_color": "#7c3aed",
        "description": "Run powerful open-source LLMs locally. No API key required.",
        "key_label": None,
        "key_placeholder": "No API key needed for local Ollama",
        "docs": "https://ollama.ai",
        "models_note": "Models auto-detected from your local Ollama install.",
    },
    "OpenAI": {
        "color": "#34d399",
        "badge_color": "#059669",
        "description": "Access GPT-4o and GPT-3.5 via the OpenAI API.",
        "key_label": "OpenAI API Key",
        "key_placeholder": "sk-...",
        "docs": "https://platform.openai.com/api-keys",
        "models_note": "Requires a valid API key to list live models.",
    },
    "Gemini": {
        "color": "#60a5fa",
        "badge_color": "#2563eb",
        "description": "Use Google's Gemini 1.5 Pro/Flash models via Google AI Studio.",
        "key_label": "Google AI Studio API Key",
        "key_placeholder": "AIza...",
        "docs": "https://aistudio.google.com/apikey",
        "models_note": "Get your free API key from Google AI Studio.",
    },
    "Claude": {
        "color": "#f9a8d4",
        "badge_color": "#db2777",
        "description": "Use Anthropic's Claude 3.5 Sonnet and Claude 3 Haiku models.",
        "key_label": "Anthropic API Key",
        "key_placeholder": "sk-ant-...",
        "docs": "https://console.anthropic.com",
        "models_note": "Get your API key from the Anthropic Console.",
    },
}


def _get_provider_models(provider_name: str, api_key: str) -> list:
    """Attempt to fetch models from the provider; fallback to static list."""
    try:
        from helpers.providers import ProviderFactory
        p = ProviderFactory.get_provider(provider_name, "", api_key)
        return p.get_model_list()
    except Exception:
        return []


def render_settings():
    """Render the AI Settings configuration page."""
    load_config()

    # ─── Header ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-size:2rem; font-weight:800; margin:0; background: linear-gradient(135deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            ⚙️ AI Provider Settings
        </h1>
        <p style="color:#94a3b8; margin-top:0.4rem;">
            Switch AI providers and models without changing any code. API keys are stored securely in your session.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ─── Current Status Banner ───────────────────────────────────────────────
    current_provider = get_current_provider_name()
    current_model = get_current_model()
    icon = PROVIDER_ICONS.get(current_provider, "🤖")
    badge_color = PROVIDER_DESCRIPTIONS.get(current_provider, {}).get("badge_color", "#334155")

    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
                border-radius:16px; padding:1.25rem 1.75rem; margin-bottom:2rem;
                display:flex; align-items:center; gap:1rem;">
        <div style="width:48px; height:48px; border-radius:50%;
                    background:{badge_color}22; display:flex; align-items:center;
                    justify-content:center; font-size:1.5rem;">{icon}</div>
        <div>
            <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:2px;">Currently Active</div>
            <div style="font-size:1.1rem; font-weight:700; color:#f1f5f9;">
                {current_provider}
                <span style="font-size:0.85rem; font-weight:400; color:#94a3b8; margin-left:0.5rem;">
                    / {current_model}
                </span>
            </div>
        </div>
        <div style="margin-left:auto; background:{badge_color}33; color:{badge_color};
                    border:1px solid {badge_color}66; border-radius:20px;
                    padding:4px 14px; font-size:0.75rem; font-weight:600;">
            ● ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── Provider Selector ───────────────────────────────────────────────────
    st.markdown("### 🔌 Select AI Provider")

    provider_cols = st.columns(4)
    selected_provider = st.session_state.get("settings_selected_provider", current_provider)

    for i, pname in enumerate(PROVIDER_NAMES):
        meta = PROVIDER_DESCRIPTIONS[pname]
        is_active = selected_provider == pname
        border = f"2px solid {meta['color']}" if is_active else "1px solid rgba(255,255,255,0.08)"
        bg = f"{meta['color']}18" if is_active else "rgba(255,255,255,0.03)"
        with provider_cols[i]:
            if st.button(
                f"{PROVIDER_ICONS[pname]} {pname}",
                key=f"provider_btn_{pname}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state["settings_selected_provider"] = pname
                st.rerun()

    # Refresh after selection
    selected_provider = st.session_state.get("settings_selected_provider", current_provider)
    meta = PROVIDER_DESCRIPTIONS[selected_provider]

    st.markdown(f"""
    <div style="background: {meta['color']}12; border: 1px solid {meta['color']}40;
                border-radius:12px; padding:1rem 1.5rem; margin:1.25rem 0;">
        <span style="font-size:1.5rem;">{PROVIDER_ICONS[selected_provider]}</span>
        <strong style="color:{meta['color']}; margin-left:0.5rem;">{selected_provider}</strong>
        <span style="color:#94a3b8;"> — {meta['description']}</span>
        <a href="{meta['docs']}" target="_blank"
           style="color:{meta['color']}; text-decoration:none; margin-left:0.75rem;
                  font-size:0.8rem;">🔗 Get API Key ↗</a>
    </div>
    """, unsafe_allow_html=True)

    # ─── API Key Input ───────────────────────────────────────────────────────
    api_key = ""
    if meta["key_label"]:
        st.markdown(f"### 🔑 {meta['key_label']}")
        api_key = st.text_input(
            label=meta["key_label"],
            value=get_current_api_key() if selected_provider == current_provider else "",
            type="password",
            placeholder=meta["key_placeholder"],
            label_visibility="collapsed",
            key="settings_api_key_input",
            help=f"Your key is stored only in session memory unless you enable persistence below. {meta['models_note']}",
        )
        st.caption(f"🔒 Stored in memory only. {meta['models_note']}")
    else:
        st.markdown("""
        <div style="background: rgba(167,139,250,0.08); border-radius:10px;
                    padding:0.75rem 1rem; color:#a78bfa; font-size:0.9rem; margin:0.5rem 0;">
            🦙 <strong>Ollama</strong> runs locally — no API key required.
            Make sure <code>ollama serve</code> is running.
        </div>
        """, unsafe_allow_html=True)

    # ─── Model Selector ─────────────────────────────────────────────────────
    st.markdown("### 🧠 Select Model")

    with st.spinner("Loading available models..."):
        models = _get_provider_models(selected_provider, api_key)

    if not models:
        models = ["Unable to load — check key or connection"]

    default_model_idx = 0
    if selected_provider == current_provider and current_model in models:
        default_model_idx = models.index(current_model)

    selected_model = st.selectbox(
        "Model",
        options=models,
        index=default_model_idx,
        key="settings_model_selector",
        label_visibility="collapsed",
    )

    # ─── Persistence Option ──────────────────────────────────────────────────
    st.markdown("### 💾 Persist Settings")
    persist = st.toggle(
        "Save settings to `.env` file (survives app restarts)",
        value=False,
        key="settings_persist_toggle",
        help="API keys will be written to a local .env file in your project directory. Never commit this file.",
    )
    if persist:
        st.warning(
            "⚠️ Your API key will be saved to `.env` on disk. "
            "Add `.env` to your `.gitignore` to keep it private.",
            icon="⚠️",
        )

    # ─── Action Buttons ──────────────────────────────────────────────────────
    st.markdown("---")
    col_test, col_save, col_reset = st.columns([1, 1, 1])

    with col_test:
        if st.button("🔌 Test Connection", use_container_width=True, key="btn_test_connection"):
            with st.spinner(f"Testing {selected_provider} / {selected_model}..."):
                try:
                    from helpers.providers import ProviderFactory
                    test_provider = ProviderFactory.get_provider(
                        selected_provider, selected_model, api_key
                    )
                    ok = test_provider.is_available()
                    if ok:
                        st.success(
                            f"✅ Connected! {PROVIDER_ICONS[selected_provider]} **{selected_provider}** "
                            f"/ `{selected_model}` is ready."
                        )
                    else:
                        st.error(
                            f"❌ Connection failed. Check your API key and ensure the "
                            f"provider service is reachable."
                        )
                except Exception as ex:
                    st.error(f"❌ Error: {str(ex)}")

    with col_save:
        if st.button("💾 Save Settings", use_container_width=True, type="primary", key="btn_save_settings"):
            save_config(
                provider=selected_provider,
                model=selected_model,
                api_key=api_key,
                persist=persist,
            )
            st.session_state["settings_selected_provider"] = selected_provider
            st.success(
                f"✅ Settings saved! Now using **{selected_provider}** / `{selected_model}`."
            )
            st.rerun()

    with col_reset:
        if st.button("🔄 Reset to Ollama", use_container_width=True, key="btn_reset_provider"):
            save_config(provider="Ollama", model="llama3.2:3b", api_key="", persist=False)
            st.session_state["settings_selected_provider"] = "Ollama"
            st.success("✅ Reset to Ollama (llama3.2:3b).")
            st.rerun()

    # ─── Provider Comparison Table ───────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📊 Provider Comparison")

    cols = st.columns([1.5, 1, 1, 1, 1])
    headers = ["Feature", "🦙 Ollama", "🤖 OpenAI", "✨ Gemini", "🌟 Claude"]
    for col, h in zip(cols, headers):
        col.markdown(f"**{h}**")

    rows = [
        ("API Key Required", "❌ No", "✅ Yes", "✅ Yes", "✅ Yes"),
        ("Runs Locally", "✅ Yes", "❌ No", "❌ No", "❌ No"),
        ("Free Tier", "✅ Free", "⚠️ Credits", "✅ Yes", "⚠️ Credits"),
        ("Best For", "Privacy", "GPT-4o Power", "Fast Flash", "Long Context"),
        ("Top Model", "llama3.2", "gpt-4o", "gemini-1.5-pro", "claude-3-5-sonnet"),
    ]

    for row in rows:
        r_cols = st.columns([1.5, 1, 1, 1, 1])
        for col, val in zip(r_cols, row):
            col.markdown(val)
