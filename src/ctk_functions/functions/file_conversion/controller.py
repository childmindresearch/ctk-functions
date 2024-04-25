"""Functions for converting files between different formats."""

import tempfile

import pypandoc


def markdown2docx(markdown: str) -> bytes:
    """Converts a Markdown document to a .docx file.

    Args:
        markdown: The Markdown document.

    Returns:
        The .docx file.
    """
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
