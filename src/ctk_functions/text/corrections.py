"""Module for syntax and grammatical correctionss of text."""

from collections.abc import Iterable

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
        self.language_tool = language_tool_python.LanguageTool(
            "en-US",
        )
        self.language_tool.enabled_rules = set(enabled_rules)
        self.language_tool.enabled_rules_only = True

    def run(self, text: str) -> str:
        """Corrects the text following the object's settings.

        Initializing the language tool takes a while, so it is performed at
        the class level. This, however, creates a race condition when multiple
        threads try to access the language tool at the same time. To prevent
        this, a lock is used to ensure that only one thread can access the
        language tool at a time.

        Args:
            text: The text to correct.

        Returns:
            The corrected text.
        """
        corrections = self.language_tool.check(text)
        while corrections:
            text = self._apply_correction(corrections[-1], text)
            corrections = self.language_tool.check(text)
        return text

    @classmethod
    def _apply_correction(
        cls,
        correction: language_tool_python.Match,
        full_text: str,
    ) -> str:
        """Applies a correction to a text.

        Args:
            correction: The language tool Match.
            full_text: The full text to correct.
        """
        if len(correction.replacements) == 1:
            # language_tool_python doesn't type hint replacements correctly.
            replacement: str = correction.replacements[0]
            return (
                full_text[: correction.offset]
                + replacement
                + full_text[correction.offset + correction.errorLength :]
            )

        if correction.ruleId == "PERS_PRONOUN_AGREEMENT":
            return cls._resolve_pers_pronoun_agreement(correction, full_text)
        msg = f"Cannot resolve replacement {correction}."
        raise ValueError(msg)

    @classmethod
    def _resolve_pers_pronoun_agreement(
        cls,
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
        verb_tense = cls._get_verb_tense(full_text, correction.offset)

        # Example correction message: "Use a third-person plural verb with ‘they’.""  # noqa: E501, RUF003

        subject = correction.message.split("‘")[1].split("’")[0].lower()  # noqa: RUF001

        if subject == "they":
            target_tense = "VBP" if verb_tense == "VBZ" else verb_tense
        elif verb_tense == "VBP":
            target_tense = "VBZ"
        else:
            target_tense = verb_tense

        # language_tool_python doesn't type hint replacements correctly.
        replacement: str
        for replacement in correction.replacements:
            new_sentence = (
                full_text[: correction.offset]
                + replacement
                + full_text[correction.offset + correction.errorLength :]
            )
            new_verb_tense = cls._get_verb_tense(new_sentence, correction.offset)
            if new_verb_tense == target_tense:
                return new_sentence

        msg = f"Could not find a suitable replacement for {correction}."
        raise ValueError(msg)

    @classmethod
    def _get_verb_tense(cls, sentence: str, verb_offset: int) -> str:
        """Gets the tense of a verb."""
        doc = NLP(sentence)
        verb = next(word for word in doc if word.idx == verb_offset)
        return verb.tag_
