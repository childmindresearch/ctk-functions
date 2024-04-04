# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.11-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY pyproject.toml poetry.lock function_app.py README.md LICENSE host.json ./
COPY src ./src
RUN pip install --no-cache-dir . && \
    python -m spacy download en_core_web_sm


COPY . /home/site/wwwroot
