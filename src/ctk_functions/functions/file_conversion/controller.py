"""Functions for converting files between different formats."""

import tempfile

import pypandoc

from ctk_functions.text import corrections


def markdown2docx(
    markdown: str, *, correct_they: bool = False, correct_capitalization: bool = False
) -> bytes:
    """Converts a Markdown document to a .docx file.

    Args:
        markdown: The Markdown document.
        correct_they: Whether to correct verb conjugations associated with 'they'.
        correct_capitalization: Whether to correct the capitalization of the text.

    Returns:
        The .docx file.
    """
    if correct_they or correct_capitalization:
        markdown = corrections.TextCorrections(
            correct_they=correct_they, correct_capitalization=correct_capitalization
        ).correct(markdown)

    with tempfile.NamedTemporaryFile(suffix=".docx") as temp_file:
        pypandoc.convert_text(
            markdown,
            "docx",
            format="md",
            outputfile=temp_file.name,
        )
        temp_file.seek(0)
        return temp_file.read()
