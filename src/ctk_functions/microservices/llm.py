"""This module coalesces all large language models from different microservices."""

from typing import Literal

from ctk_functions import config
from ctk_functions.microservices import aws, azure, utils

VALID_LLM_MODELS = Literal["gpt-4o", "anthropic.claude-3-opus-20240229-v1:0"]

logger = config.get_logger()


class LargeLanguageModel(utils.LlmAbstractBaseClass):
    """Llm class that provides access to all available LLMs.

    Attributes:
        client: The client for the large language model.
    """

    def __init__(self, model: VALID_LLM_MODELS) -> None:
        """Initializes the language model.

        Args:
            model: The model to use for the language model.
        """
        self.client: azure.AzureLlm | aws.ClaudeLlm
        if model == "gpt-4o":
            logger.info("Using Azure LLM")
            self.client = azure.AzureLlm()
        elif model == "anthropic.claude-3-opus-20240229-v1:0":
            logger.info("Using AWS LLM")
            self.client = aws.ClaudeLlm()
        else:
            raise ValueError(f"Invalid LLM model: {model}")

    async def run(self, system_prompt: str, user_prompt: str) -> str:
        """Runs the model with the given prompts.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.

        Returns:
            The output text.
        """
        return await self.client.run(system_prompt, user_prompt)
