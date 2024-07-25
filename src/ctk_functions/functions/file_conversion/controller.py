"""Functions for converting files between different formats."""

import pathlib
import re
import tempfile
from typing import Any

import cmi_docx
import docx
import pypandoc


def markdown2docx(
    markdown: str, formatting: None | dict[str, Any] | cmi_docx.ParagraphStyle = None
) -> bytes:
    """Converts a Markdown document to a .docx file.

    Uses a custom lua filter to allow underlining text between two '++'.

    Args:
        markdown: The Markdown document.
        formatting: Formatting options, must abide by cmi_docx.ParagraphStyle arguments
            if it is provided as a dictionary.

    Returns:
        The .docx file as bytes.
    """
    underline_filter = pathlib.Path(__file__).parent / "lua" / "underline.lua"
    tab_filter = pathlib.Path(__file__).parent / "lua" / "tab.lua"
    with tempfile.NamedTemporaryFile(suffix=".docx") as docx_file:
        pypandoc.convert_text(
            markdown,
            "docx",
            format="commonmark_x",
            outputfile=docx_file.name,
            filters=[str(underline_filter), str(tab_filter)],
        )

        docx_file.seek(0)
        mark_warnings_as_red(docx_file.name)

        if formatting is not None:
            if isinstance(formatting, dict):
                formatting = cmi_docx.ParagraphStyle(**formatting)
            document = docx.Document(docx_file.name)
            for paragraph in document.paragraphs:
                extend_paragraph = cmi_docx.ExtendParagraph(paragraph)
                extend_paragraph.format(formatting)
            document.save(docx_file.name)
        return docx_file.read()


def mark_warnings_as_red(docx_file: str | pathlib.Path) -> None:
    """Marks warning templates as red.

    We use {{!WARNING-TEXT}} as a template for warnings that should be marked red.

    Args:
        docx_file: The .docx file.
    """
    document = docx.Document(str(docx_file))
    extend_document = cmi_docx.ExtendDocument(document)
    text = "\n".join([paragraph.text for paragraph in document.paragraphs])
    warningRegex = re.compile(r"{{!.*?}}")
    matches = warningRegex.finditer(text)
    uniqueMatches = set([match.group() for match in matches])

    for match in uniqueMatches:
        extend_document.replace(match, match, cmi_docx.RunStyle(font_rgb=(255, 0, 0)))

    document.save(str(docx_file))
