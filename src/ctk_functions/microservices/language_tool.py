"""Provides a class for correcting text using the LanguageTool API."""

import pydantic
import requests

from ctk_functions import config

settings = config.get_settings()

LANGUAGE_TOOL_ENDPOINT = str(settings.LANGUAGE_TOOL_ENDPOINT)


@pydantic.dataclasses.dataclass
class Url:
    """Represents a URL from the LanguageTool API."""

    value: str


@pydantic.dataclasses.dataclass
class Category:
    """Represents a category from the LanguageTool API."""

    id: str
    name: str


@pydantic.dataclasses.dataclass
class Replacement:
    """Represents a replacement from the LanguageTool API."""

    value: str
    shortDescription: str | None = None


@pydantic.dataclasses.dataclass
class Context:
    """Represents a context from the LanguageTool API."""

    text: str
    offset: int
    length: int


@pydantic.dataclasses.dataclass
class Rule:
    """Represents a rule from the LanguageTool API."""

    id: str
    description: str
    issueType: str
    category: Category
    urls: list[Url] | None = None
    subId: str | None = None
    sourceFile: str | None = None


@pydantic.dataclasses.dataclass
class Correction:
    """Represents a correction from the LanguageTool API."""

    message: str
    shortMessage: str
    replacements: list[Replacement]
    rule: Rule
    offset: int
    length: int
    context: Context
    sentence: str
    ignoreForIncompleteSentence: bool
    contextForSureMatch: int


class LanguageCorrecter:
    """Corrects text using the LanguageTool API."""

    def __init__(self, url: str = LANGUAGE_TOOL_ENDPOINT) -> None:
        """Initializes the correcter with the LanguageTool API URL."""
        self.url = url

    def check(self, text: str, localization: str = "en-US") -> list[Correction]:
        """Corrects the text using the LanguageTool API.

        Args:
            text: The text to check.
            localization: The localization of the text. Defaults to "en-US".

        Returns:
            The suggested corrections.
        """
        response = requests.post(
            self.url,
            data={
                "text": text,
                "language": localization,
            },
        )

        response.raise_for_status()
        results = response.json()
        return [Correction(**result) for result in results["matches"]]
