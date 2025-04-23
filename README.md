# Clinician Toolkit API (CTK Functions)

A FastAPI service providing backend services for CTK, including document conversion, intake form processing, grammatical correction, and text generation.

## Features

- **Document Conversion**: Convert between formats (e.g., Markdown to DOCX) with custom formatting and styling
- **Intake Processing**: Transform REDCap survey data into structured clinical reports
- **Language Tool Integration**: Grammatical and syntax correction services
- **LLM Integration**: AI-assisted text generation via cloai-service

## Architecture

CTK Functions is structured as a modular FastAPI application with these key components:

- **Core**: Configuration, middleware, and shared utilities
- **Microservices**: Connectors to external services (REDCap, Language Tool, LLM)
- **Routers**: API endpoints organized by functionality
  - File Conversion
  - Health Check
  - Intake Processing
  - Language Tool
  - LLM

## License

This project is licensed under the LGPL-2.1 License - see the [LICENSE](LICENSE) file for details.
