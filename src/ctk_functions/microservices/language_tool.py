"""Module for syntax and grammatical corrections of text."""

from collections.abc import Iterable
from types import TracebackType

import aiohttp
import pydantic
import spacy
import tenacity

NLP = spacy.load("en_core_web_sm", enable=["tagger"])

# These rules are unlikely to interfere with each other and can be executed without
# rerunning LanguageTool.
SIMULTANEOUS_RULES = (
    "THE_US",
    "UPPERCASE_SENTENCE_START",
    "WEEK_HYPHEN",
    "CONSECUTIVE_SPACES",
)


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


class ReplacementData(pydantic.BaseModel):
    """The start, end, and text of a replacement.

    Used to pass replacement data to the caller who can then perform the replacement
    themselves.
    """

    start: int
    end: int
    text: str


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
        self._session = aiohttp.ClientSession()

    async def __aenter__(self) -> "LanguageCorrecter":
        """Return self when entering the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Close the underlying HTTP session when exiting the context."""
        await self._session.close()

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=5),
    )
    async def check(self, text: str) -> LanguageToolResponse:
        """Sends a request to LanguageTool and returns the response.

        Args:
            text: The text to check.

        Returns:
            The response from LanguageTool.
        """
        response = await self._session.post(
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

    async def provide_replacements(self, text: str) -> list[ReplacementData]:
        """Corrects the text and returns the required replacements.

        Replacements may interfere with each other and, as such, should always be
        applied in the order listed.

        Args:
            text: The text to correct.

        Returns:
            The correct replacements.
        """
        response = await self.check(text)
        replacements = []
        while response.matches:
            alterations = [
                match
                for match in response.matches
                if match.rule.id in SIMULTANEOUS_RULES
            ]
            not_simultaneous_matches = [
                match
                for match in response.matches
                if match.rule.id not in SIMULTANEOUS_RULES
            ]

            if not_simultaneous_matches:
                alterations.append(not_simultaneous_matches[-1])
            alterations.sort(key=lambda match: match.offset, reverse=True)

            for match in alterations:
                correction_index = self._get_correction_index(match, text)
                replacements.append(
                    ReplacementData(
                        start=match.offset,
                        end=match.offset + match.length,
                        text=match.replacements[correction_index].value,
                    ),
                )
                text = self._apply_correction(text, match, correction_index)

            if len(response.matches) == len(alterations):
                # Do not re-check if there was only one non-simultaneous correction
                # remaining.
                break
            response = await self.check(text)

        return replacements

    async def correct(self, text: str) -> str:
        """Corrects the text following the object's settings.

        Args:
            text: The text to correct.

        Returns:
            The corrected text.
        """
        replacements = await self.provide_replacements(text)
        for replacement in replacements:
            text = (
                text[: replacement.start] + replacement.text + text[replacement.end :]
            )
        return text

    @staticmethod
    def _apply_correction(text: str, correction: Match, index: int) -> str:
        return (
            text[: correction.offset]
            + correction.replacements[index].value
            + text[correction.offset + correction.length :]
        )

    @classmethod
    def _get_correction_index(
        cls,
        correction: Match,
        full_text: str,
    ) -> int:
        """Get a correction for the text.

        Args:
            correction: The language tool Match.
            full_text: The full text to correct.

        Returns:
            The corrected text.
        """
        if len(correction.replacements) == 1:
            return 0
        if correction.rule.id == "PERS_PRONOUN_AGREEMENT":
            return cls._resolve_pers_pronoun_agreement(correction, full_text)
        msg = f"Cannot resolve replacement {correction}."
        raise ValueError(msg)

    @classmethod
    def _resolve_pers_pronoun_agreement(
        cls,
        correction: Match,
        full_text: str,
    ) -> int:
        """Resolves personal pronoun corrections with multiple replacements.

        Consult https://www.nltk.org/book/ch05.html for more information on NLTK tokens.

        Args:
            correction: The language tool Match.
            full_text: The full text to correct.

        Returns:
            The index of the selected replacement.

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

        for index, replacement in enumerate(correction.replacements):
            new_sentence = (
                full_text[: correction.offset]
                + replacement.value
                + full_text[correction.offset + correction.length :]
            )
            new_verb_tense = cls._get_verb_tense(new_sentence, correction.offset)
            if new_verb_tense == target_tense:
                return index

        msg = f"Could not find a suitable replacement for {correction}."
        raise ValueError(msg)

    @staticmethod
    def _get_verb_tense(sentence: str, verb_offset: int) -> str:
        """Gets the tense of a verb."""
        doc = NLP(sentence)
        verb = next(word for word in doc if word.idx == verb_offset)
        return verb.tag_
