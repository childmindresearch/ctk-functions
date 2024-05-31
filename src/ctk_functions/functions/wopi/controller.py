"""Controller functions for the WOPI API."""

from ctk_functions.microservices import azure


async def get_file_metadata(filename: str) -> dict:
    """Fetches the metadata of a file from Azure Blob Storage.

    Args:
        filename: The name of the file.

    Returns:
        The file metadata.
    """
    client = azure.AzureBlobService()
    metadata = await client.read_blob_metadata("templates", filename)
    file_size = metadata.get("size", 0)
    return {
        "BaseFileName": filename,
        "OwnerId": 1000,
        "UserId": 1000,
        "Size": file_size,
        "UserCanWrite": True,
    }


async def get_file_contents(filename: str) -> bytes:
    """Fetches the contents of a file from Azure Blob Storage.

    Args:
        filename: The name of the file.

    Returns:
        The file contents.
    """
    client = azure.AzureBlobService()
    return await client.read_blob("templates", filename)


async def put_file_contents(filename: str, contents: bytes) -> None:
    """Updates the contents of a file in Azure Blob Storage.

    Args:
        filename: The name of the file.
        contents: The new contents of the file.
    """
    client = azure.AzureBlobService()
    await client.update_blob("templates", filename, contents)
