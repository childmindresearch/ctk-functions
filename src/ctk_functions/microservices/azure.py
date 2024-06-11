"""A module to interact with Azure Blob Storage."""

import openai
from azure.storage.blob import aio

from ctk_functions import config

logger = config.get_logger()

settings = config.get_settings()
AZURE_BLOB_CONNECTION_STRING = settings.AZURE_BLOB_CONNECTION_STRING
AZURE_OPENAI_API_KEY = settings.AZURE_OPENAI_API_KEY
AZURE_OPENAI_LLM_DEPLOYMENT = settings.AZURE_OPENAI_LLM_DEPLOYMENT
AZURE_OPENAI_ENDPOINT = settings.AZURE_OPENAI_ENDPOINT


class AzureError(Exception):
    """An exception to raise when an error occurs in the Azure service."""

    pass


class AzureLlm:
    """A class to interact with the Azure Language Model service."""

    def __init__(
        self,
    ) -> None:
        """Initialize the Azure Language Model client.

        Args:
            deployment: The deployment name.
            endpoint: The endpoint URL.
        """
        self.client = openai.AsyncAzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY.get_secret_value(),
            azure_endpoint=AZURE_OPENAI_ENDPOINT.get_secret_value(),
            api_version="2024-02-01",
        )

    async def run(self, system_prompt: str, user_prompt: str) -> str:
        """Runs the model with the given prompts.

        Args:
            system_prompt: The system prompt.
            user_prompt: The user prompt.

        Returns:
            The output text.
        """
        system_message = {
            "role": "system",
            "content": system_prompt,
        }
        user_message = {
            "role": "user",
            "content": user_prompt,
        }
        try:
            response = await self.client.chat.completions.create(
                messages=[system_message, user_message],  # type: ignore
                model=AZURE_OPENAI_LLM_DEPLOYMENT.get_secret_value(),
            )
            message = response.choices[0].message.content
        except openai.BadRequestError:
            # Fallback: Return a message to the user even on remote server failure.
            # Example of this being necessary is content management policy.
            message = "Failure in LLM processing. Please let the development team know."

        if message is None:
            message = "Failure in LLM processing. Please let the development team know."
        return message


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
