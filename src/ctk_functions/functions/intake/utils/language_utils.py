"""Utilities for correcting grammar and syntax."""

import asyncio

import cmi_docx
import docx
import spacy
from docx import document

from ctk_functions.text import corrections

NLP = spacy.load("en_core_web_sm", enable=["parser"])

# c.f. https://community.languagetool.org/rule/list?lang=en for a list of rules.
# These are the rules that have been tested on existing intake reports and are
# used for the dynamic text. Rules applying only to static template text
# should be fixed in the template itself.

DEFAULT_LANGUAGE_RULES = {
    "BASE_FORM",
    "CONSECUTIVE_SPACES",
    "PERS_PRONOUN_AGREEMENT",
    "NON3PRS_VERB",
    "THE_US",
    "UPPERCASE_SENTENCE_START",
    "WEEK_HYPHEN",
}


class DocumentCorrections:
    """Corrects verb conjugations associated with 'they' in a Word document."""

    def __init__(
        self,
        document: document.Document,
        enabled_rules: set[str] = DEFAULT_LANGUAGE_RULES,
    ) -> None:
        """Initializes the corrector with a document.

        Args:
            document: The docx document to correct.
            enabled_rules: The rules to enable for the correction. If None, all rules
                are enabled.

        """
        self.document = document
        self.correcter = corrections.LanguageCorrecter(enabled_rules)

    async def correct(self) -> None:
        """Makes corrections based on the enabled rules."""
        promises = [
            self._correct_paragraph(paragraph) for paragraph in self.document.paragraphs
        ]
        await asyncio.gather(*promises)

    async def _correct_paragraph(
        self, paragraph: docx.text.paragraph.Paragraph
    ) -> None:
        """Corrects conjugations in a single paragraph.

        Args:
            paragraph: The paragraph to correct.
        """
        sentences = NLP(paragraph.text)

        async def correct_with_old(sentence: str) -> tuple[str, str]:
            return sentence, await self.correcter.run(sentence)

        new_sentences_promises = [
            correct_with_old(sentence.text) for sentence in sentences.sents
        ]
        extended_pargraph = cmi_docx.ExtendParagraph(paragraph)

        for correction in asyncio.as_completed(new_sentences_promises):
            old, new = await correction
            extended_pargraph.replace(old, new)
