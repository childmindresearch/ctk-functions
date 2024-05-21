"""Test the WOPI controller functions."""

import pytest
import pytest_mock

from ctk_functions.functions.wopi import controller


@pytest.mark.asyncio
async def test_get_file_metadata(mocker: pytest_mock.MockFixture) -> None:
    """Test the file metadata is found correctly."""
    mocker.patch(
        "ctk_functions.microservices.azure.AzureBlobService.read_blob_metadata",
        return_value={"size": 1024},
    )
    filename = "test_file.txt"
    expected = {
        "BaseFileName": filename,
        "OwnerId": 1000,
        "UserId": 1000,
        "Size": 1024,
        "UserCanWrite": True,
    }

    metadata = await controller.get_file_metadata(filename)

    assert metadata == expected


@pytest.mark.asyncio
async def test_get_file_contents(mocker: pytest_mock.MockFixture) -> None:
    """Test the file contents are found correctly."""
    mocker.patch(
        "ctk_functions.microservices.azure.AzureBlobService.read_blob",
        return_value=b"test file contents",
    )
    filename = "test_file.txt"
    expected = b"test file contents"

    contents = await controller.get_file_contents(filename)

    assert contents == expected
