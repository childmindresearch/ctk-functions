"""Test a few survey IDs. This is run only on Azure Pipelines."""

import asyncio
import os

from ctk_functions.core import config
from ctk_functions.routers.intake import controller

settings = config.get_settings()
survey_ids = [s.strip() for s in os.environ["SURVEY_IDS"].split(",")]

promises = [
    controller.get_intake_report(
        survey_id,
    )
    for survey_id in survey_ids
]

asyncio.get_event_loop().run_until_complete(asyncio.gather(*promises))
