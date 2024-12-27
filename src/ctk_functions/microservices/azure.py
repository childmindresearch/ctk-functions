"""A module to interact with Azure Blob Storage."""

from typing import Literal

import openai

from ctk_functions import config
from ctk_functions.microservices import utils

logger = config.get_logger()

settings = config.get_settings()
AZURE_OPENAI_API_KEY = settings.AZURE_OPENAI_API_KEY
AZURE_OPENAI_LLM_DEPLOYMENT = settings.AZURE_OPENAI_LLM_DEPLOYMENT
AZURE_OPENAI_ENDPOINT = settings.AZURE_OPENAI_ENDPOINT

GPT_MODELS = Literal["gpt-4o"]


class AzureLlm(utils.LlmAbstractBaseClass):
    """A class to interact with the Azure Language Model service."""

    def __init__(
        self,
        model: GPT_MODELS = "gpt-4o",
    ) -> None:
        """Initialize the Azure Language Model client.

        Args:
            model: The model to use for the language model.
        """
        self.client = openai.AsyncAzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY.get_secret_value(),
            azure_endpoint=AZURE_OPENAI_ENDPOINT.get_secret_value(),
            api_version="2024-02-01",
        )
        self.model = model

    async def run(self, system_prompt: str, user_prompt: str) -> str:
        """Runs the model with the given prompts.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.

        Returns:
            The output text.
        """
        system_message = {
            "role": "system",
            "content": system_prompt,
        }
        user_message = {
            "role": "user",
            "content": user_prompt,
        }
        try:
            response = await self.client.chat.completions.create(
                messages=[system_message, user_message],  # type: ignore[list-item]
                model=AZURE_OPENAI_LLM_DEPLOYMENT.get_secret_value(),
            )
            message = response.choices[0].message.content
        except openai.BadRequestError:
            # Fallback: Return a message to the user even on remote server failure.
            # Example of this being necessary is content management policy.
            message = "Failure in LLM processing. Please let the development team know."

        if message is None:
            message = "Failure in LLM processing. Please let the development team know."
        return message
