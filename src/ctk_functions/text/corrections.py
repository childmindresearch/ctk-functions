"""Module for syntax and grammatical correctionss of text."""

import asyncio
from typing import Iterable

import language_tool_python
import spacy

NLP = spacy.load("en_core_web_sm", enable=["tagger"])


class LanguageCorrecter:
    """Corrects the grammar and syntax of text."""

    def __init__(
        self,
        enabled_rules: Iterable[str],
    ) -> None:
        """Initializes the language tool.

        Args:
            enabled_rules: The rules to enable for the correction.

        """
        self.language_tool = language_tool_python.LanguageTool("en-US")
        self.language_tool.enabled_rules = set(enabled_rules)
        self.language_tool.enabled_rules_only = True

    async def _check(self, text: str) -> list[language_tool_python.Match]:
        """Checks the text for errors.

        Args:
            text: The text to check.

        Returns:
            A list of errors in the text.
        """
        return await asyncio.get_event_loop().run_in_executor(
            None, self.language_tool.check, text
        )

    async def run(self, text: str) -> str:
        """Corrects the text following the object's settings.

        Args:
            text: The text to correct.

        Returns:
            The corrected text.
        """
        if not text:
            return text

        corrections = await self._check(text)
        while corrections:
            text = self._apply_correction(corrections[-1], text)
            corrections = await self._check(text)
        return text

    def _apply_correction(
        self, correction: language_tool_python.Match, full_text: str
    ) -> str:
        """Applies a correction to a text.

        Args:
            correction: The language tool Match.
            full_text: The full text to correct.
        """
        if len(correction.replacements) == 1:
            return (
                full_text[: correction.offset]
                + correction.replacements[0]
                + full_text[correction.offset + correction.errorLength :]
            )

        if correction.ruleId == "PERS_PRONOUN_AGREEMENT":
            return self._resolve_pers_pronoun_agreement(correction, full_text)
        else:
            raise ValueError(f"Cannot resolve replacement {correction}.")

    def _resolve_pers_pronoun_agreement(
        self,
        correction: language_tool_python.Match,
        full_text: str,
    ) -> str:
        """Resolves personal pronoun corrections with multiple replacements.

        Consult https://www.nltk.org/book/ch05.html for more information on NLTK tokens.

        Args:
            correction: The language tool Match.
            full_text: The full text to correct.

        Returns:
            The corrected text.
        """
        verb_tense = self._get_verb_tense(full_text, correction.offset)

        # Example correction message: "Use a third-person plural verb with ‘they’.""

        subject = correction.message.split("‘")[1].split("’")[0].lower()

        if subject == "they":
            target_tense = "VBP" if verb_tense == "VBZ" else verb_tense
        elif verb_tense == "VBP":
            target_tense = "VBZ"
        else:
            target_tense = verb_tense

        for replacement in correction.replacements:
            new_sentence = (
                full_text[: correction.offset]
                + replacement
                + full_text[correction.offset + correction.errorLength :]
            )
            new_verb_tense = self._get_verb_tense(new_sentence, correction.offset)
            if new_verb_tense == target_tense:
                return new_sentence

        raise ValueError(f"Could not find a suitable replacement for {correction}.")

    @staticmethod
    def _get_verb_tense(sentence: str, verb_offset: int) -> str:
        """Gets the tense of a verb."""
        doc = NLP(sentence)
        verb = next(word for word in doc if word.idx == verb_offset)
        return verb.tag_
