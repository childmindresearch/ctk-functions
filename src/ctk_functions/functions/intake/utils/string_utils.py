"""Utilities for working with strings."""

import re


class StringToInt:
    """Converts a string to a numeric."""

    def __init__(self, *, allow_fallback: bool = True) -> None:
        """Initializes the string to numeric converter.

        Args:
            allow_fallback: Whether to return the original string if it cannot be
                parsed to an integer.
        """
        self.allow_fallback = allow_fallback

    class StringParseError(Exception):
        """Exception raised when a string cannot be parsed to a number."""

    @property
    def word_mapping(self) -> dict[str, int]:
        """The mapping of string numbers to integers.

        This does not support numbers greater than 99.
        """
        return {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "thirteen": 13,
            "fourteen": 14,
            "fifteen": 15,
            "sixteen": 16,
            "seventeen": 17,
            "eighteen": 18,
            "nineteen": 19,
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60,
            "seventy": 70,
            "eighty": 80,
            "ninety": 90,
        }

    def parse(self, string: str) -> float | int | str:
        """Parses a string to an integer or float.

        Args:
            string: The string to parse.
            allow_fallback: Whether to return the original string if it cannot be
                parsed to an integer.

        Returns:
            The integer/float value of the string.
        """
        try:
            integers = self.parse_integers(string)
            if isinstance(integers, int):
                return integers
        except self.StringParseError:
            pass

        try:
            floats = self.parse_floats(string)
            if isinstance(floats, float):
                return floats
        except self.StringParseError:
            pass

        try:
            words = self.parse_words(string)
            if isinstance(words, int):
                return words
        except self.StringParseError:
            pass

        return self._return_string_or_raise(string)

    def parse_integers(self, string: str) -> int | str:
        """Parses a string to an integer by extracting all numerics.

        Note: this will not handle negative numbers.

        Args:
            string: The string to parse.

        Returns:
            The integer value of the string.
        """
        numerics = [char for char in string if char.isnumeric()]
        if "".join(numerics) not in string:
            return self._return_string_or_raise(string)

        if numerics:
            return int("".join(numerics))
        return self._return_string_or_raise(string)

    def parse_floats(self, string: str) -> float | str:
        """Parses a string to a float by extracting all numerics.

        Note: this will not handle negative numbers.

        Args:
            string: The string to parse.

        Returns:
            The float value of the string.
        """
        parts = string.split(".")
        if len(parts) != 2:  # noqa: PLR2004
            return self._return_string_or_raise(string)

        integer_part = self.parse_integers(parts[0])
        decimal_part = self.parse_integers(parts[1])
        if isinstance(integer_part, int) and isinstance(decimal_part, int):
            return float(f"{integer_part}.{decimal_part}")
        return self._return_string_or_raise(string)

    def parse_words(self, string: str) -> int | str:
        """Parses a string to an integer.

        Args:
            string: The string to parse.

        Returns:
            The integer value of the string.
        """
        words = re.split(r" |-", string.lower())

        parsed_words = [self.word_mapping.get(word, None) for word in words]

        if None in parsed_words:
            return self._return_string_or_raise(string)
        return sum(parsed_words)  # type: ignore[arg-type] # Mypy mistakenly believes this can contain None.

    def _return_string_or_raise(self, string: str) -> str:
        if self.allow_fallback:
            return string
        msg = f"Could not parse {string} to an integer."
        raise self.StringParseError(msg)


def join_with_oxford_comma(
    items: list[str],
) -> str:
    """Joins a list of items with an Oxford comma.

    Args:
        items: The items to be joined.

    Returns:
        str: The joined string.
    """
    if len(items) == 0:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:  # noqa: PLR2004
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def ordinal_suffix(number: int | str) -> str:
    """Converts a number to its ordinal suffix.

    Args:
        number: The number to convert.

    Returns:
        str: The ordinal suffix of the number.
    """
    number = int(number)

    last_two_digits = number % 100
    if 11 <= last_two_digits <= 13:  # noqa: PLR2004
        return "th"

    last_digit = number % 10
    if last_digit == 1:
        return "st"
    if last_digit == 2:  # noqa: PLR2004
        return "nd"
    if last_digit == 3:  # noqa: PLR2004
        return "rd"
    return "th"


def remove_excess_whitespace(text: str) -> str:
    """Removes excess whitespace from a string."""
    return " ".join(text.split())
