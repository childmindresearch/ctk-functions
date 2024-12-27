"""Performs basic tests on the intake_writer.py module.

These tests are intended to be run as a smoke test to ensure that the module's
basic functionality is working as expected. It also contains a few basic checks
for easy-to-make mistakes.
"""

import re
from collections.abc import Coroutine
from typing import TypeVar

import pytest
import pytest_mock
from docx import document

from ctk_functions.functions.intake import parser, writer
from ctk_functions.microservices import redcap

T = TypeVar("T")


@pytest.fixture
async def intake_document(
    mocker: pytest_mock.MockFixture,
    test_redcap_data: redcap.RedCapData,
) -> document.Document:
    """Returns a file-like object for the intake_writer.py module."""
    mocker.patch(
        "ctk_functions.microservices.azure.AzureLlm.run",
        return_value="llm",
    )
    mocker.patch(
        "ctk_functions.microservices.llm.LargeLanguageModel.chain_of_verification",
        return_value="cov",
    )
    mocker.patch(
        "ctk_functions.microservices.llm.LargeLanguageModel.call_instructor",
        return_value="instructor",
    )
    intake_info = parser.IntakeInformation(test_redcap_data)
    intake_writer = writer.ReportWriter(intake_info, "gpt-4o")
    await intake_writer.transform()
    return intake_writer.report.document  # type: ignore[no-any-return]


@pytest.mark.asyncio
async def test_no_printed_objects(
    intake_document: Coroutine[document.Document, None, None],
) -> None:
    """Tests that the document contains no printed objects.

    Some of these tests (e.g. None) may need to be removed if they are
    expected to be in the document in the future. This test is not
    comprehensive, but it should catch some easy mistakes.
    """
    regex_scientific_notation = r"\de[-\d]"

    text = "\n".join([p.text.lower() for p in (await intake_document).paragraphs])  # type: ignore[attr-defined, func-returns-value]

    assert "[]" not in text
    assert "{" not in text
    assert "}" not in text
    assert "<" not in text
    assert ">" not in text
    assert "none" not in text
    assert "ctk_api" not in text
    assert "object at 0x" not in text
    assert "replacementtags" not in text
    assert re.match(regex_scientific_notation, text) is None


@pytest.mark.asyncio
async def test_expected_strings_in_document(
    intake_document: Coroutine[document.Document, None, None],
    test_redcap_data: redcap.RedCapData,
) -> None:
    """Tests that the document contains some expected strings."""
    text = "\n".join([p.text for p in (await intake_document).paragraphs])  # type: ignore[attr-defined, func-returns-value]
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
    assert test_redcap_data.firstname in text
    assert test_redcap_data.lastname in text
