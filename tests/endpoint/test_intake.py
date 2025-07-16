"""Tests for the intake endpoints."""

import pathlib

import docx
import pytest_mock
from fastapi import status, testclient

from ctk_functions.routers.intake.intake_processing import writer_llm


def test_intake_with_model(
    client: testclient.TestClient,
    tmp_path: pathlib.Path,
    mocker: pytest_mock.MockerFixture,
) -> None:
    """Tests whether the GET intake endpoint works with a model."""
    mocker.patch(
        "ctk_functions.microservices.cloai_service.Client.chain_of_verification",
        return_value="cov",
    )
    mocker.patch(
        "ctk_functions.microservices.cloai_service.Client.call_instructor",
        return_value="instructor",
    )
    mocker.patch(
        "ctk_functions.microservices.cloai_service.Client.run",
        return_value="run",
    )
    mocker.patch.object(
        writer_llm.WriterLlm, "classify_family_relatedness", return_value="1st"
    )

    response = client.get(
        "/intake-report/mock",
        headers={"X-model": "anthropic.claude-3-5-sonnet-20241022-v2:0"},
    )
    with (tmp_path / "file.docx").open("wb") as file:
        file.write(response.read())

    assert response.status_code == status.HTTP_200_OK
    docx.Document(str(tmp_path / "file.docx"))  # Test that it's a valid .docx file.
