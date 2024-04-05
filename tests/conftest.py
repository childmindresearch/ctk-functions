"""Configuration for pytest."""

import pathlib
from typing import Any

import pytest

from ctk_functions.microservices import redcap


@pytest.fixture(scope="session")
def test_redcap_data() -> dict[str, Any]:
    """Returns a dictionary of test data."""
    data_file = pathlib.Path(__file__).parent / "data" / "test_redcap_data.csv"
    contents = data_file.read_text().strip()
    dataframe = redcap.parse_redcap_dtypes(contents)
    return dataframe.row(0, named=True)
