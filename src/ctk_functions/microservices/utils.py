"""Utilities for the microservices."""

import abc
from typing import Any


class LlmAbstractBaseClass(abc.ABC):
    """An abstract class for large language model interfaces."""

    @abc.abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
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
