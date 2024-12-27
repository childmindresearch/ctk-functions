"""This module contains interactions with AWS microservices."""

from typing import Literal

import anthropic

from ctk_functions.core import config
from ctk_functions.microservices import utils

settings = config.get_settings()

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
ANTHROPIC_MODELS = Literal[
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    "anthropic.claude-3-opus-20240229-v1:0",
]


class ClaudeLlm(utils.LlmAbstractBaseClass):
    """Caller for Claude Large Language models.

    Attributes:
        client: The BedRock client.
        model: The model that is invoked.

    """

    def __init__(
        self,
        model: ANTHROPIC_MODELS,
    ) -> None:
        """Initializes the BedRock client."""
        if model in (
            "anthropic.claude-3-opus-20240229-v1:0",
            "anthropic.claude-3-5-sonnet-20241022-v2:0",
        ):
            region = "us-west-2"
        elif model == "anthropic.claude-3-5-sonnet-20240620-v1:0":
            region = "us-east-1"
        else:
            msg = "Unknown model."
            raise ValueError(msg)

        self.client = anthropic.AsyncAnthropicBedrock(
            aws_access_key=AWS_ACCESS_KEY_ID.get_secret_value(),
            aws_secret_key=AWS_SECRET_ACCESS_KEY.get_secret_value(),
            aws_region=region,
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
        message = await self.client.messages.create(
            model=self.model,
            max_tokens=5000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        return message.content[0].text  # type: ignore[union-attr]
