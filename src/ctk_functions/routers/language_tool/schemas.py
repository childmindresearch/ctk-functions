"""Schemas for the language tool endpoint."""

import pydantic


class PostLanguageToolRequest(pydantic.BaseModel):
    """POST LanguageTool request definition.

    Attributes:
        text: The text to correct.
        rules: The rules to enable c.f. LanguageTool for a list of rules.
    """

    text: str
    rules: tuple[str, ...] = pydantic.Field(..., min_length=1)
