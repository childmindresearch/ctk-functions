"""Endpoint tests for file conversion."""

from fastapi import status, testclient


def test_language_tool_post(client: testclient.TestClient) -> None:
    """Tests the POST markdown2docx endpoint."""
    text = "Hello , world!"
    expected = "Hello, world!"

    response = client.post(
        "/language-tool",
        json={"text": text, "rules": ("COMMA_PARENTHESIS_WHITESPACE",)},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected
