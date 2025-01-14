"""Tests for the health endpoint."""

from fastapi import status, testclient


def test_health(client: testclient.TestClient) -> None:
    """Tests whether the health endpoint returns 200."""
    response = client.get("/health")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["cloai_service"]
    assert data["language_tool"]
