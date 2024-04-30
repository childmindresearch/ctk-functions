"""Utilities for correcting grammar and syntax."""

import docx
import spacy
from cmi_docx import ExtendParagraph

from ctk_functions.text import corrections

NLP = spacy.load("en_core_web_sm")


class DocumentCorrections:
    """Corrects verb conjugations associated with 'they' in a Word document."""

    def __init__(
        self,
        document: docx.Document,
        *,
        correct_they: bool = True,
        correct_capitalization: bool = True,
    ) -> None:
        """Initializes the corrector with a document.

        Args:
            document: The docx document to correct.
            correct_they: Whether to correct verb conjugations associated with 'they'.
            correct_capitalization: Whether to correct the capitalization of the text.

        """
        self.document = document
        self.corrector = corrections.TextCorrections(
            correct_they=correct_they,
            correct_capitalization=correct_capitalization,
        )

    def correct(self) -> None:
        """Corrects verb conjugations associated with 'they' in the document."""
        for paragraph in self.document.paragraphs:
            self._correct_paragraph(paragraph)

    def _correct_paragraph(self, paragraph: docx.text.paragraph.Paragraph) -> None:
        """Corrects conjugations in a single paragraph.

        Args:
            paragraph: The paragraph to correct.
        """
        sentences = NLP(paragraph.text).sents
        new_sentences = [
            self.corrector.correct(sentence.text) for sentence in sentences
        ]
        extended_pargraph = ExtendParagraph(paragraph)
        for old, new in zip(sentences, new_sentences):
            if old.text != new:
                extended_pargraph.replace(old.text, new)
