# Dockerfile for building the ctk-functions container.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm as builder

WORKDIR /app
ARG AZURE_BLOB_SIGNATURES_CONNECTION_STRING

COPY uv.lock pyproject.toml LICENSE README.md ./
COPY src src
RUN mkdir -p src/ctk_functions/data/signatures

RUN apt-get update; apt-get install -y curl unzip
RUN mkdir /downloads
RUN curl -o /downloads/azure-blob-signatures.zip $AZURE_BLOB_SIGNATURES_CONNECTION_STRING
RUN unzip /downloads/azure-blob-signatures.zip
RUN mv *.png src/ctk_functions/data/signatures
RUN uv sync --frozen --no-cache --no-dev


FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

EXPOSE 8000
WORKDIR /app
COPY --from=builder /app /app

CMD ["uv", "run", "fastapi", "run", "src/ctk_functions/app.py", "--port", "8000",  "--host", "0.0.0.0"]
