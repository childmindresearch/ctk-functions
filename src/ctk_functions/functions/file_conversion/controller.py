"""Functions for converting files between different formats."""

import re
import tempfile

import cmi_docx
import docx
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
        mark_warnings_as_red(temp_file.name)
        return temp_file.read()


def mark_warnings_as_red(docx_file: str) -> None:
    """Marks warning templates as red.

    We use {{!WARNING-TEXT}} as a template for warnings that should be marked red.

    Args:
        docx_file: The .docx file.
    """
    document = docx.Document(docx_file)
    extend_document = cmi_docx.ExtendDocument(document)
    text = "\n".join([paragraph.text for paragraph in document.paragraphs])
    warningRegex = re.compile(r"{{!.*?}}")
    matches = set(warningRegex.finditer(text))
    for match in matches:
        extend_document.replace(match.group(), match.group(), {"font_rgb": (255, 0, 0)})
    document.save(docx_file)
