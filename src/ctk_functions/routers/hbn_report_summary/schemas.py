"""Schemas for the LLM endpoint."""

import pydantic


class PostReportSummaryRequest(pydantic.BaseModel):
    """POST LLM request definition.

    Attributes:
        user_prompt: The user's message.
    """

    user_prompt: str
