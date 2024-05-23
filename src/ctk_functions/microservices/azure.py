"""A module to interact with Azure Blob Storage."""

from azure.storage.blob import aio

from ctk_functions import config

logger = config.get_logger()

settings = config.get_settings()
AZURE_BLOB_CONNECTION_STRING = settings.AZURE_BLOB_CONNECTION_STRING


class AzureBlobService:
    """A class to interact with Azure Blob Storage."""

    def __init__(
        self, connection_string: str = AZURE_BLOB_CONNECTION_STRING.get_secret_value()
    ) -> None:
        """Initialize the Azure Blob Service.

        Args:
            connection_string: The connection string to the Azure Blob Service.
        """
        logger.debug("Initializing Azure Blob Service.")
        self.client = aio.BlobServiceClient.from_connection_string(connection_string)

    async def read_blob(self, container_name: str, blob_name: str) -> bytes:
        """Reads the contents of a blob from the specified container.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.

        Returns:
            The contents of the blob as bytes.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return await (await blob_client.download_blob()).readall()

    async def read_blob_metadata(self, container_name: str, blob_name: str) -> dict:
        """Reads the metadata of a blob from the specified container.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.

        Returns:
            The metadata of the blob as a dictionary.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_properties = await blob_client.get_blob_properties()
        return blob_properties.metadata

    async def create_blob(
        self, container_name: str, blob_name: str, data: bytes
    ) -> None:
        """Creates a new blob in the specified container with the given data.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.
            data: The data to be uploaded as bytes.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        await blob_client.upload_blob(data, overwrite=False)

    async def update_blob(
        self, container_name: str, blob_name: str, data: bytes
    ) -> None:
        """Updates an existing blob in the specified container with the given data.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.
            data: The data to be uploaded as bytes.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        await blob_client.upload_blob(data, overwrite=True)

    async def delete_blob(self, container_name: str, blob_name: str) -> None:
        """Deletes a blob from the specified container.

        Args:
            container_name: The name of the container.
            blob_name: The name of the blob.
        """
        container_client = self.client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        await blob_client.delete_blob()

    async def directory_contents(self, container_name: str) -> list[str]:
        """List the contents of a container in Azure Blob Storage.

        Args:
            container_name: The name of the container.

        Returns:
            A list of blob names.
        """
        logger.debug(f"Listing contents of container {container_name}.")
        container_client = self.client.get_container_client(container_name)
        blobs = container_client.list_blobs()
        return [blob.name async for blob in blobs]

    async def close(self) -> None:
        """Close the Azure Blob Service."""
        logger.debug("Closing Azure Blob Service.")
        await self.client.close()
