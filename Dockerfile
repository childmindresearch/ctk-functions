# Dockerfile for building the ctk-functions container which runs Azure Functions using Python 3.11.
#
# Stages:
# 1. `unzipper`: Downloads and unzips Azure Blob Signatures.
# 2. `mcr.microsoft.com/azure-functions/python:4-python3.11`: Final image that will run on Azure.
#
# Build Arguments:
# - `AZURE_BLOB_SIGNATURES_CONNECTION_STRING`: Connection string that lets the container download the signatures file.
FROM alpine:latest as unzipper

WORKDIR /files
ARG AZURE_BLOB_SIGNATURES_CONNECTION_STRING

RUN apk add --no-cache unzip curl
RUN curl -o /files/azure-blob-signatures.zip $AZURE_BLOB_SIGNATURES_CONNECTION_STRING
RUN unzip /files/azure-blob-signatures.zip

FROM mcr.microsoft.com/azure-functions/python:4-python3.12

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true
ENV PATH="/$HOME/.cargo/bin/:$PATH"

COPY . /home/site/wwwroot
RUN mkdir -p /home/site/wwwroot/src/ctk_functions/data/signatures
COPY --from=unzipper /files/*.png /home/site/wwwroot/src/ctk_functions/data/signatures

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN cd /home/site/wwwroot && \
    apt-get clean; apt-get -y update && \
    mkdir -p /usr/share/man/man1/ && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y openjdk-17-jre && \
    update-alternatives --config java && \
    update-alternatives --config javac && \
    sh /uv-installer.sh && rm /uv-installer.sh && \
    uv sync --no-dev --frozen --no-cache --python-preference system && \
    uv run python -m spacy download en_core_web_sm && \
    uv run python -c 'import spacy; spacy.load("en_core_web_sm")' && \
    uv run python -c 'import language_tool_python; language_tool_python.LanguageTool("en-US")'
