"""This module coalesces all large language models from different microservices."""

import typing
from typing import TypeGuard

from ctk_functions import config
from ctk_functions.microservices import aws, azure, utils

VALID_LLM_MODELS = typing.Literal[aws.ANTHROPIC_MODELS, azure.GPT_MODELS]

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
        if self._is_azure_model(model):
            self.client = azure.AzureLlm(model)
        elif self._is_aws_model(model):
            self.client = aws.ClaudeLlm(model)
        else:
            # As the model name can be supplied by the user, this case might be reached.
            msg = f"Invalid LLM model: {model}"
            raise ValueError(msg)

    async def run(self, system_prompt: str, user_prompt: str) -> str:
        """Runs the model with the given prompts.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.

        Returns:
            The output text.
        """
        return await self.client.run(system_prompt, user_prompt)

    @staticmethod
    def _is_azure_model(model: VALID_LLM_MODELS) -> TypeGuard[azure.GPT_MODELS]:
        return model in typing.get_args(azure.GPT_MODELS)

    @staticmethod
    def _is_aws_model(model: VALID_LLM_MODELS) -> TypeGuard[aws.ANTHROPIC_MODELS]:
        return model in typing.get_args(aws.ANTHROPIC_MODELS)
