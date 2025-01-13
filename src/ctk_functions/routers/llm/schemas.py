"""Schemas for the LLM endpoint."""

import pydantic


class PostLlmRequest(pydantic.BaseModel):
    """POST LLM request definition.

    Attributes:
        model: The Large Language Model to use.
        system_prompt: The model instructions.
        user_prompt: The user's message.
    """

    system_prompt: str
    user_prompt: str
