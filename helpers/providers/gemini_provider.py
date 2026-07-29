"""
Google Gemini provider — uses the google-generativeai SDK.
Requires: GEMINI_API_KEY (Google AI Studio)
Supported models: gemini-1.5-pro, gemini-1.5-flash, gemini-pro
"""
from helpers.providers.base_provider import BaseProvider

GEMINI_MODELS = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-pro",
]


class GeminiProvider(BaseProvider):
    """
    Provider wrapping Google's Generative AI (Gemini) API.
    """

    def __init__(self, model: str = "gemini-1.5-flash", api_key: str = ""):
        super().__init__(model=model, api_key=api_key)

    def _client(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            return genai
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai>=0.7.0"
            )

    def chat_completion(self, prompt: str) -> str:
        genai = self._client()
        model = genai.GenerativeModel(
            model_name=self.model,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2,
            )
        )
        response = model.generate_content(prompt)
        return response.text or ""

    def is_available(self) -> bool:
        if not self.api_key:
            return False
        try:
            genai = self._client()
            # Quick list check to verify key validity
            list(genai.list_models())
            return True
        except Exception:
            return False

    def get_model_list(self) -> list:
        if not self.api_key:
            return GEMINI_MODELS
        try:
            genai = self._client()
            models = [
                m.name.replace("models/", "")
                for m in genai.list_models()
                if "generateContent" in m.supported_generation_methods
            ]
            return models if models else GEMINI_MODELS
        except Exception:
            return GEMINI_MODELS
