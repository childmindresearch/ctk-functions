"""Schemas for the LLM endpoint."""

import pydantic

from ctk_functions.microservices import language_models


class PostLlmRequest(pydantic.BaseModel):
    """POST LLM request definition.

    Attributes:
        model: The Large Language Model to use.
        system_prompt: The model instructions.
        user_prompt: The user's message.
    """

    model: language_models.VALID_MODELS
    system_prompt: str
    user_prompt: str
