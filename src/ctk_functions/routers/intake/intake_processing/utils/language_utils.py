"""Utilities for correcting grammar and syntax."""

import asyncio

import cmi_docx
import spacy
from docx import document
from docx.text import paragraph

from ctk_functions.core import config
from ctk_functions.text import corrections

settings = config.get_settings()
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
        doc: document.Document,
        enabled_rules: set[str] | None = None,
    ) -> None:
        """Initializes the corrector with a document.

        Args:
            doc: The docx document to correct.
            enabled_rules: The rules to enable for the correction. If None, all rules
                are enabled.

        """
        self.document = doc
        self.correcter = corrections.LanguageCorrecter(
            enabled_rules or DEFAULT_LANGUAGE_RULES,
            settings.LANGUAGE_TOOL_URL,
        )

    async def correct(self) -> None:
        """Makes corrections based on the enabled and disabled rules."""
        await asyncio.gather(
            *[self._correct_paragraph(para) for para in self.document.paragraphs],
        )

    async def _correct_paragraph(self, para: paragraph.Paragraph) -> None:
        """Corrects conjugations in a single paragraph.

        Args:
            para: The paragraph to correct.
        """
        sentences = list(NLP(para.text).sents)
        new_sentences = [
            await self.correcter.correct(sentence.text) for sentence in sentences
        ]
        extended_pargraph = cmi_docx.ExtendParagraph(para)
        for old, new in zip(sentences, new_sentences, strict=True):
            if old.text != new:
                extended_pargraph.replace(old.text, new)
