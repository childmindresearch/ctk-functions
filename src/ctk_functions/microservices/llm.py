"""This module coalesces all large language models from different microservices."""

import typing

from ctk_functions import config
from ctk_functions.microservices import aws, azure, utils

VALID_LLM_MODELS = aws.ANTHROPIC_MODELS | azure.GPT_MODELS

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
        logger.info("Using LLM model: %s", model)
        if model in typing.get_args(azure.GPT_MODELS):
            self.client = azure.AzureLlm(model)  # type: ignore[arg-type] # mypy doesn't detect typing.get_args() as type narrowing.
        elif model in typing.get_args(aws.ANTHROPIC_MODELS):
            self.client = aws.ClaudeLlm(model)  # type: ignore[arg-type] # mypy doesn't detect typing.get_args() as type narrowing.
        else:
            # As the model name can be supplied by the user, this case might be reached.
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
