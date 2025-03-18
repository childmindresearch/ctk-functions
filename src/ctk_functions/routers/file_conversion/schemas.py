"""Schemas for the file conversion router."""

import cmi_docx
import pydantic


class PostMarkdown2DocxRequest(pydantic.BaseModel):
    """Definition of the markdown2docx request.

    Attributes:
        markdown: The markdown to convert to .docx.
        formatting: Formatting for the text.
    """

    markdown: str
    formatting: cmi_docx.ParagraphStyle | None = None


class PostReferralTableDocxRequest(pydantic.BaseModel):
    """Definition of the referral table request.

    Attributes:
        title: The title of the referral table.
        row_data: The contents of the referral table as a list of rows.
    """

    title: str
    row_data: list[list[str]]
