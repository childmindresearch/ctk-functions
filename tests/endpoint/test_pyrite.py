"""Tests for the Pyrite endpoints."""

import pathlib

import docx
from fastapi import status, testclient


def test_get_pyrite(
    client: testclient.TestClient, tmp_path: pathlib.Path, mock_sql_calls: None
) -> None:
    """Test the Pyrite GET endpoint."""
    response = client.get("/pyrite/12345")
    with (tmp_path / "file.docx").open("wb") as file:
        file.write(response.read())

    assert response.status_code == status.HTTP_200_OK
    docx.Document(str(tmp_path / "file.docx"))  # Test that it's a valid .docx file.
