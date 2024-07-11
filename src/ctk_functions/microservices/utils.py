"""Utilities for the microservices."""

import abc


class LlmAbstractBaseClass(abc.ABC):
    """An abstract class for large language model interfaces."""

    model: str

    @abc.abstractmethod
    def __init__(self, model: str) -> None:
        """Initialize the Language Model client."""
        pass

    @abc.abstractmethod
    async def run(self, system_prompt: str, user_prompt: str) -> str:
        """Runs the model with the given prompts.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.
        """
        pass
