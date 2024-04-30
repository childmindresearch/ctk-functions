"""Functions for converting files between different formats."""

import tempfile

import pypandoc

from ctk_functions.text import corrections


def markdown2docx(markdown: str) -> bytes:
    """Converts a Markdown document to a .docx file.

    Args:
        markdown: The Markdown document.

    Returns:
        The .docx file.
    """
    if "they" in markdown.lower():
        markdown = corrections.TextCorrections(correct_they=True).correct(markdown)

    with tempfile.NamedTemporaryFile(suffix=".docx") as temp_file:
        pypandoc.convert_text(
            markdown,
            "docx",
            format="md",
            outputfile=temp_file.name,
            extra_args=["-f", "markdown+grid_tables"],
        )
        temp_file.seek(0)
        return temp_file.read()
