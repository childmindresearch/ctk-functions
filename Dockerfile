FROM mcr.microsoft.com/azure-functions/python:4-python3.11

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY . /home/site/wwwroot

RUN cd /home/site/wwwroot && \
    apt-get clean; apt-get -y update && \
    mkdir -p /usr/share/man/man1/ && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y openjdk-17-jre && \
    update-alternatives --config java && \
    update-alternatives --config javac && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi && \
    poetry run python -c 'import spacy; spacy.load("en_core_web_sm")' && \
    poetry run python -c 'import language_tool_python; language_tool_python.LanguageTool("en-US")'
