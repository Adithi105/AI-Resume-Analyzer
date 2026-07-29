"""
OpenAI provider — uses OpenAI Chat Completions API.
Requires: OPENAI_API_KEY
Supported models: gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo
"""
from helpers.providers.base_provider import BaseProvider

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo",
]


class OpenAIProvider(BaseProvider):
    """
    Provider wrapping the OpenAI Chat Completions API.
    """

    def __init__(self, model: str = "gpt-4o-mini", api_key: str = ""):
        super().__init__(model=model, api_key=api_key)

    def _client(self):
        try:
            from openai import OpenAI
            return OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "openai package not installed. Run: pip install openai>=1.40.0"
            )

    def chat_completion(self, prompt: str) -> str:
        client = self._client()
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        return response.choices[0].message.content or ""

    def is_available(self) -> bool:
        if not self.api_key:
            return False
        try:
            client = self._client()
            client.models.retrieve(self.model)
            return True
        except Exception:
            return False

    def get_model_list(self) -> list:
        if not self.api_key:
            return OPENAI_MODELS
        try:
            client = self._client()
            models = client.models.list()
            chat_models = sorted(
                [m.id for m in models.data if "gpt" in m.id],
                reverse=True
            )
            return chat_models if chat_models else OPENAI_MODELS
        except Exception:
            return OPENAI_MODELS
