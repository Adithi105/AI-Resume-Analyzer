"""
Config Manager — handles secure storage and retrieval of provider settings and API keys.

Storage strategy:
  1. Runtime: st.session_state (always used, ephemeral per session).
  2. Persistent: .env file in project root (optional user choice, survives restarts).

API keys are NEVER logged, printed, or committed to source code.
"""
import os
import streamlit as st

# Session state keys
_KEY_PROVIDER = "ai_provider"
_KEY_MODEL = "ai_model"
_KEY_API_KEY = "ai_api_key"
_KEY_PERSIST = "ai_persist_key"

# Env variable names
ENV_PROVIDER = "AI_PROVIDER"
ENV_MODEL = "AI_MODEL"
ENV_OPENAI_KEY = "OPENAI_API_KEY"
ENV_GEMINI_KEY = "GEMINI_API_KEY"
ENV_CLAUDE_KEY = "ANTHROPIC_API_KEY"

_ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


def _provider_env_key(provider: str) -> str:
    mapping = {
        "openai": ENV_OPENAI_KEY,
        "gemini": ENV_GEMINI_KEY,
        "claude": ENV_CLAUDE_KEY,
    }
    return mapping.get(provider.lower(), "")


def load_config():
    """
    Load provider configuration into session_state on first run.
    Priority: session_state > .env file > defaults.
    """
    if _KEY_PROVIDER in st.session_state:
        return  # Already loaded this session

    # Try to load from .env
    try:
        from dotenv import dotenv_values
        if os.path.exists(_ENV_FILE):
            env_vals = dotenv_values(_ENV_FILE)
            provider = env_vals.get(ENV_PROVIDER, "Ollama")
            model = env_vals.get(ENV_MODEL, "llama3.2:3b")
            env_key = _provider_env_key(provider)
            api_key = env_vals.get(env_key, "") if env_key else ""
            st.session_state[_KEY_PROVIDER] = provider
            st.session_state[_KEY_MODEL] = model
            st.session_state[_KEY_API_KEY] = api_key
            st.session_state[_KEY_PERSIST] = True
            return
    except Exception:
        pass

    # Defaults
    st.session_state[_KEY_PROVIDER] = "Ollama"
    st.session_state[_KEY_MODEL] = "llama3.2:3b"
    st.session_state[_KEY_API_KEY] = ""
    st.session_state[_KEY_PERSIST] = False


def save_config(provider: str, model: str, api_key: str, persist: bool = False):
    """
    Save provider configuration to session state and optionally to .env file.

    Args:
        provider: Provider display name (e.g. 'OpenAI').
        model: Selected model name.
        api_key: Provider API key (empty string for Ollama).
        persist: If True, also write to .env file.
    """
    st.session_state[_KEY_PROVIDER] = provider
    st.session_state[_KEY_MODEL] = model
    st.session_state[_KEY_API_KEY] = api_key
    st.session_state[_KEY_PERSIST] = persist

    if persist:
        _write_env(provider, model, api_key)


def _write_env(provider: str, model: str, api_key: str):
    """Write config to .env file (creates or updates)."""
    try:
        lines = []
        if os.path.exists(_ENV_FILE):
            with open(_ENV_FILE, "r") as f:
                lines = f.readlines()

        # Keys to update
        updates = {ENV_PROVIDER: provider, ENV_MODEL: model}
        env_key = _provider_env_key(provider)
        if env_key and api_key:
            updates[env_key] = api_key

        # Update existing keys
        new_lines = []
        updated_keys = set()
        for line in lines:
            key_part = line.split("=")[0].strip()
            if key_part in updates:
                new_lines.append(f'{key_part}={updates[key_part]}\n')
                updated_keys.add(key_part)
            else:
                new_lines.append(line)

        # Append any new keys
        for k, v in updates.items():
            if k not in updated_keys:
                new_lines.append(f'{k}={v}\n')

        with open(_ENV_FILE, "w") as f:
            f.writelines(new_lines)
    except Exception as e:
        pass  # Silent fail — .env is optional


def get_active_provider():
    """
    Return a ready-to-use provider instance from current session state config.

    Returns:
        BaseProvider instance.
    """
    from helpers.providers import ProviderFactory
    provider = st.session_state.get(_KEY_PROVIDER, "Ollama")
    model = st.session_state.get(_KEY_MODEL, "llama3.2:3b")
    api_key = st.session_state.get(_KEY_API_KEY, "")
    return ProviderFactory.get_provider(provider, model, api_key)


def get_current_provider_name() -> str:
    return st.session_state.get(_KEY_PROVIDER, "Ollama")


def get_current_model() -> str:
    return st.session_state.get(_KEY_MODEL, "llama3.2:3b")


def get_current_api_key() -> str:
    return st.session_state.get(_KEY_API_KEY, "")


def clear_config():
    """Reset provider config to defaults."""
    for k in [_KEY_PROVIDER, _KEY_MODEL, _KEY_API_KEY, _KEY_PERSIST]:
        if k in st.session_state:
            del st.session_state[k]
