"""Tests for the LLM endpoints."""

import pytest_mock
from fastapi import status, testclient

from ctk_functions.routers.llm import schemas


def test_llm(client: testclient.TestClient, mocker: pytest_mock.MockerFixture) -> None:
    """Test the LLM endpoint."""
    spy = mocker.patch(
        "cloai.LargeLanguageModel.run",
        return_value="output",
    )
    body = schemas.PostLlmRequest(
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        system_prompt="sys",
        user_prompt="user",
    )
    response = client.post("/llm", json=body.model_dump())

    assert response.status_code == status.HTTP_200_OK
    assert response.text == '"output"'
    assert spy.call_count == 1
