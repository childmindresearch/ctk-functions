"""Test a few survey IDs. This is run only on Azure Pipelines."""

import asyncio
import os

from ctk_functions.routers.intake import controller
from ctk_functions.text import corrections

corrections.LanguageCorrecter(enabled_rules=set())  # Download LanguageTool
survey_ids = [s.strip() for s in os.environ["SURVEY_IDS"].split(",")]

promises = [
    controller.get_intake_report(
        survey_id,
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
    )
    for survey_id in survey_ids
]

asyncio.get_event_loop().run_until_complete(asyncio.gather(*promises))
