"""A module to interact with Azure Blob Storage."""

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

    async def close(self) -> None:
        """Close the Azure Blob Service."""
        await self.blob_service_client.close()
