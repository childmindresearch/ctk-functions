"""Schemas for the file conversion router."""

from typing import TypeVar

import cmi_docx
import pydantic

ParagraphStyleType = TypeVar("ParagraphStyleType", bound=cmi_docx.ParagraphStyle)


class PostMarkdown2DocxRequest(pydantic.BaseModel):
    """Definition of the markdown2docx request.

    Attributes:
        markdown: The markdown to convert to .docx.
        formatting: Formatting for the text.
    """

    markdown: str
    formatting: cmi_docx.ParagraphStyle | None = None
