"""
Ollama provider — wraps local Ollama server for self-hosted models.
Requires: ollama running locally (`ollama serve`).
No API key needed.
"""
from helpers.providers.base_provider import BaseProvider

OLLAMA_DEFAULT_MODELS = [
    "llama3.2:3b",
    "llama3.2:1b",
    "llama3.1:8b",
    "llama3.1:70b",
    "mistral:7b",
    "mixtral:8x7b",
    "gemma2:9b",
    "gemma2:27b",
    "qwen2.5:7b",
    "phi3:mini",
    "codellama:7b",
]


class OllamaProvider(BaseProvider):
    """
    Provider wrapping Ollama's local inference server.
    """

    def __init__(self, model: str = "llama3.2:3b", api_key: str = ""):
        super().__init__(model=model, api_key=api_key)

    def chat_completion(self, prompt: str) -> str:
        import ollama
        try:
            response = ollama.chat(
                model=self.model,
                format="json",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.get("message", {}).get("content", "")
        except Exception:
            # Retry without format enforcement
            import ollama as _ollama
            response = _ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.get("message", {}).get("content", "")

    def is_available(self) -> bool:
        try:
            import ollama
            ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": "ping"}]
            )
            return True
        except Exception:
            return False

    def get_model_list(self) -> list:
        try:
            import ollama
            models_resp = ollama.list()
            models = models_resp.get("models", [])
            if models:
                return [m.get("name", m.get("model", "")) for m in models if m.get("name") or m.get("model")]
        except Exception:
            pass
        return OLLAMA_DEFAULT_MODELS
