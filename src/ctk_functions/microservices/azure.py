"""A module to interact with Azure Blob Storage."""

import pathlib

import aiofiles
from azure.storage.blob import aio


class AzureBlobService:
    """A class to interact with Azure Blob Storage."""

    def __init__(self, connection_string: str) -> None:
        """Initialize the Azure Blob Service.

        Args:
            connection_string: The connection string to the Azure Blob Service.
        """
        self.blob_service_client = aio.BlobServiceClient.from_connection_string(
            connection_string
        )

    async def download_blob(self, container_name: str, blob_name: str) -> bytes:
        """Download a blob from Azure Blob Storage.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.

        Returns:
            The content of the blob.
        """
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        return await (await blob_client.download_blob()).readall()

    async def save_blob_to_disk(
        self, container_name: str, blob_name: str, file_path: pathlib.Path | str
    ) -> pathlib.Path:
        """Save a blob from Azure Blob Storage to disk.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.
            file_path: The path to save the blob to.

        Returns:
            The path to the saved file.
        """
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(await self.download_blob(container_name, blob_name))
        return pathlib.Path(file_path)

    async def directory_contents(self, container_name: str) -> list[str]:
        """List the contents of a container in Azure Blob Storage.

        Args:
            container_name: The name of the container.

        Returns:
            A list of blob names.
        """
        container_client = self.blob_service_client.get_container_client(container_name)
        blobs = container_client.list_blobs()
        return [blob.name async for blob in blobs]
