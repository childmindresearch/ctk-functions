"""Performs basic tests on the intake_writer.py module.

These tests are intended to be run as a smoke test to ensure that the module's
basic functionality is working as expected. It also contains a few basic checks
for easy-to-make mistakes.
"""

import re
from collections.abc import Generator
from typing import Any

import docx
import pytest

from ctk_functions.intake import parser, writer


@pytest.fixture(scope="module")
def intake_document(
    test_redcap_data: dict[str, Any],
) -> Generator[docx.Document, None, None]:
    """Returns a file-like object for the intake_writer.py module."""
    intake_info = parser.IntakeInformation(test_redcap_data)
    intake_writer = writer.ReportWriter(intake_info)
    intake_writer.transform()
    return intake_writer.report


def test_no_printed_objects(intake_document: docx.Document) -> None:
    """Tests that the document contains no printed objects.

    Some of these tests (e.g. None) may need to be removed if they are
    expected to be in the document in the future. This test is not
    comprehensive, but it should catch some easy mistakes.
    """
    regex_scientific_notation = r"\de[-\d]"
    text = "\n".join([p.text for p in intake_document.paragraphs])

    assert "[]" not in text
    assert "{" not in text
    assert "}" not in text
    assert "<" not in text
    assert ">" not in text
    assert "None" not in text
    assert "ctk_api" not in text
    assert "object at 0x" not in text
    assert re.match(regex_scientific_notation, text) is None


def test_expected_strings_in_document(
    intake_document: docx.Document,
    test_redcap_data: dict[str, Any],
) -> None:
    """Tests that the document contains some expected strings."""
    text = "\n".join([p.text for p in intake_document.paragraphs])
    headers = [
        "REASON FOR VISIT",
        "IDENTIFYING INFORMATION",
        "DEVELOPMENTAL HISTORY",
        "RECOMMENDATIONS",
        "MENTAL STATUS EXAMINATION AND TESTING BEHAVIORAL OBSERVATIONS",
        "Strategies and Resources Appendix",
    ]

    assert all(header in text for header in headers)
    assert "Director, Center for the Developing Brain" in text
    assert test_redcap_data["firstname"] in text
    assert test_redcap_data["lastname"] in text
