"""
Abstract base class for all AI provider implementations.
All providers must implement this interface contract.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseProvider(ABC):
    """
    Abstract base provider defining the interface all AI providers must implement.
    """

    def __init__(self, model: str, api_key: str = ""):
        self.model = model
        self.api_key = api_key

    @abstractmethod
    def chat_completion(self, prompt: str) -> str:
        """
        Send a prompt and return the raw text response from the model.

        Args:
            prompt: The full prompt string.

        Returns:
            str: Raw model response text.
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider and model are reachable.

        Returns:
            bool: True if the provider is accessible.
        """
        ...

    @abstractmethod
    def get_model_list(self) -> list:
        """
        Return a list of available model names for this provider.

        Returns:
            list[str]: Model names.
        """
        ...
