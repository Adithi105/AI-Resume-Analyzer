"""
Anthropic Claude provider — uses the anthropic SDK.
Requires: ANTHROPIC_API_KEY
Supported models: claude-3-5-sonnet, claude-3-haiku, claude-3-opus
"""
from helpers.providers.base_provider import BaseProvider

CLAUDE_MODELS = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]


class ClaudeProvider(BaseProvider):
    """
    Provider wrapping Anthropic's Claude Messages API.
    """

    def __init__(self, model: str = "claude-3-5-haiku-20241022", api_key: str = ""):
        super().__init__(model=model, api_key=api_key)
        self._max_tokens = 4096

    def _client(self):
        try:
            import anthropic
            return anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Run: pip install anthropic>=0.34.0"
            )

    def chat_completion(self, prompt: str) -> str:
        client = self._client()
        message = client.messages.create(
            model=self.model,
            max_tokens=self._max_tokens,
            messages=[{"role": "user", "content": prompt}],
            system=(
                "You are an expert AI assistant. Always respond with valid raw JSON only. "
                "Do NOT include markdown code fences or any commentary outside the JSON object."
            ),
        )
        return message.content[0].text if message.content else ""

    def is_available(self) -> bool:
        if not self.api_key:
            return False
        try:
            client = self._client()
            client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "ping"}]
            )
            return True
        except Exception:
            return False

    def get_model_list(self) -> list:
        return CLAUDE_MODELS
