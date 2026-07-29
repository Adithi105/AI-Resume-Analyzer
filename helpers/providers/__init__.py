"""
Provider package registry and ProviderFactory.
Central factory for resolving provider names to concrete provider instances.
"""
from helpers.providers.base_provider import BaseProvider

PROVIDER_NAMES = ["Ollama", "OpenAI", "Gemini", "Claude"]

PROVIDER_ICONS = {
    "Ollama": "🦙",
    "OpenAI": "🤖",
    "Gemini": "✨",
    "Claude": "🌟",
}


class ProviderFactory:
    """
    Factory class responsible for resolving provider name strings to concrete
    BaseProvider subclass instances.
    """

    @staticmethod
    def get_provider(provider_name: str, model: str, api_key: str = "") -> BaseProvider:
        """
        Instantiate and return the appropriate provider object.

        Args:
            provider_name: One of 'Ollama', 'OpenAI', 'Gemini', 'Claude'.
            model: Model name string (e.g. 'gpt-4o', 'llama3.2:3b').
            api_key: API key for cloud providers; empty string for Ollama.

        Returns:
            BaseProvider: A concrete provider instance.
        """
        name = provider_name.strip().lower()

        if name == "ollama":
            from helpers.providers.ollama_provider import OllamaProvider
            return OllamaProvider(model=model, api_key=api_key)

        elif name == "openai":
            from helpers.providers.openai_provider import OpenAIProvider
            return OpenAIProvider(model=model, api_key=api_key)

        elif name == "gemini":
            from helpers.providers.gemini_provider import GeminiProvider
            return GeminiProvider(model=model, api_key=api_key)

        elif name == "claude":
            from helpers.providers.claude_provider import ClaudeProvider
            return ClaudeProvider(model=model, api_key=api_key)

        else:
            raise ValueError(
                f"Unknown provider '{provider_name}'. "
                f"Supported providers: {PROVIDER_NAMES}"
            )
