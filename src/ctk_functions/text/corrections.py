"""Module for syntax and grammatical corrections of text."""

from collections.abc import Iterable

import aiohttp
import pydantic
import spacy

NLP = spacy.load("en_core_web_sm", enable=["tagger"])


class Software(pydantic.BaseModel):
    """Information on the language tool software."""

    name: str
    version: str
    build_date: str = pydantic.Field(alias="buildDate")
    api_version: int = pydantic.Field(alias="apiVersion")
    status: str
    premium: bool


class DetectedLanguage(pydantic.BaseModel):
    """The detected langauge."""

    name: str
    code: str


class Language(pydantic.BaseModel):
    """The language."""

    name: str
    code: str
    detected_language: DetectedLanguage = pydantic.Field(alias="detectedLanguage")


class Replacement(pydantic.BaseModel):
    """The replacement text."""

    value: str


class Context(pydantic.BaseModel):
    """The context of a match."""

    text: str
    offset: int
    length: int


class Url(pydantic.BaseModel):
    """Url to the explanation of a rule."""

    value: str | None


class Category(pydantic.BaseModel):
    """Category of a rule."""

    id: str
    name: str


class Rule(pydantic.BaseModel):
    """The violoated rule."""

    id: str
    sub_id: str | None = pydantic.Field(None, alias="subId")
    description: str
    urls: list[Url] | None = None
    issue_type: str = pydantic.Field(alias="issueType")
    category: Category


class Match(pydantic.BaseModel):
    """Match object containing data on a violated rule."""

    message: str
    short_message: str = pydantic.Field(alias="shortMessage")
    offset: int
    length: int
    replacements: list[Replacement]
    context: Context
    sentence: str
    rule: Rule


class LanguageToolResponse(pydantic.BaseModel):
    """The complete response from LanguageTool."""

    software: Software
    language: Language
    matches: list[Match]


class LanguageCorrecter:
    """Corrects the grammar and syntax of text."""

    def __init__(
        self,
        enabled_rules: Iterable[str],
        url: str,
    ) -> None:
        """Initializes the language tool.

        Args:
            enabled_rules: The rules to enable for the correction.
            url: The remote server to connect to.

        """
        self.url = url
        self.language_tool = "en-US"
        self.enabled_rules = set(enabled_rules)

    async def check(self, text: str) -> LanguageToolResponse:
        """Sends a request to LanguageTool and returns the response.

        Args:
            text: The text to check.

        Returns:
            The response from LanguageTool.
        """
        async with aiohttp.ClientSession() as client:
            response = await client.post(
                url=self.url + "/check",
                data={
                    "text": text,
                    "language": "en-US",
                    "enabledRules": ",".join(self.enabled_rules),
                    "enabledOnly": "true",
                },
            )
            text = await response.text()

        return LanguageToolResponse.model_validate_json(text)

    async def correct(self, text: str) -> str:
        """Corrects the text following the object's settings.

        Args:
            text: The text to correct.

        Returns:
            The corrected text.
        """
        response = await self.check(text)
        while response.matches:
            text = self._apply_correction(response.matches[-1], text)
            response = await self.check(text)
        return text

    @classmethod
    def _apply_correction(
        cls,
        correction: Match,
        full_text: str,
    ) -> str:
        """Applies a correction to a text.

        Args:
            correction: The language tool Match.
            full_text: The full text to correct.

        Returns:
            The corrected text.
        """
        if len(correction.replacements) == 1:
            # language_tool_python doesn't type hint replacements correctly.
            replacement: str = correction.replacements[0].value
            return (
                full_text[: correction.offset]
                + replacement
                + full_text[correction.offset + correction.length :]
            )

        if correction.rule.id == "PERS_PRONOUN_AGREEMENT":
            return cls._resolve_pers_pronoun_agreement(correction, full_text)
        msg = f"Cannot resolve replacement {correction}."
        raise ValueError(msg)

    @classmethod
    def _resolve_pers_pronoun_agreement(
        cls,
        correction: Match,
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
        for replacement in correction.replacements:
            new_sentence = (
                full_text[: correction.offset]
                + replacement.value
                + full_text[correction.offset + correction.length :]
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
