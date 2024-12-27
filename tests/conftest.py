"""Configuration for pytest."""

import pytest
from fastapi import testclient

from ctk_functions import app
from ctk_functions.microservices import redcap


@pytest.fixture(scope="session")
def test_redcap_data() -> redcap.RedCapData:
    """Returns a dictionary of test data."""
    return redcap.get_intake_data("mock")


@pytest.fixture(scope="session")
def client() -> testclient.TestClient:
    """Returns a test client."""
    return testclient.TestClient(app.app)
