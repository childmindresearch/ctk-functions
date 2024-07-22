"""Functions for converting files between different formats."""

import pathlib
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
    enabled_rules = []
    if correct_they:
        enabled_rules += ["BASE_FORM", "PERS_PRONOUN_AGREEMENT", "NON3PRS_VERB"]
    if correct_capitalization:
        enabled_rules += ["UPPERCASE_SENTENCE_START"]
    if enabled_rules:
        correcter = corrections.LanguageCorrecter(enabled_rules)
        markdown = correcter.run(markdown)

    with tempfile.NamedTemporaryFile(suffix=".docx") as temp_file:
        pypandoc.convert_text(
            markdown,
            "docx",
            format="commonmark_x",
            outputfile=temp_file.name,
        )
        temp_file.seek(0)
        mark_warnings_as_red(temp_file.name)
        return temp_file.read()


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
        extend_document.replace(match, match, {"font_rgb": (255, 0, 0)})

    document.save(str(docx_file))
