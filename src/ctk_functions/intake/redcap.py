"""This module contains functions for interacting with REDcap."""

import io

import polars as pl
import requests

from ctk_functions import config

settings = config.get_settings()
REDCAP_ENDPOINT = settings.REDCAP_ENDPOINT


def get_intake_data(survey_id: str) -> pl.DataFrame:
    """Gets the intake data from REDcap.

    Args:
        survey_id: The survey ID.

    Returns:
        The intake data for the survey.
    """
    data = {
        "token": settings.REDCAP_API_TOKEN.get_secret_value(),
        "content": "record",
        "format": "csv",
        "type": "flat",
        "records": survey_id,
    }

    response = requests.post(str(REDCAP_ENDPOINT), data=data)
    response.raise_for_status()
    return parse_redcap_dtypes(response.text)


def parse_redcap_dtypes(csv_data: str) -> pl.DataFrame:
    """Parses the REDcap data with the appropriate data types.

    REDCap data types are finnicky due to the large number of freeform string inputs and
    the .csv format. This function parses the data with the appropriate data types.
    All data that isn't explicitly typed by this function is set to a string.

    Args:
        csv_data: The CSV data to parse.

    Returns:
        The parsed REDcap data.
    """
    dtypes = {
        "age": pl.Float32,
        "biohx_dad_other": pl.Int8,
        "biohx_mom_other": pl.Int8,
        "birth_location": pl.Int8,
        "child_language1_fluency": pl.Int8,
        "child_language2_fluency": pl.Int8,
        "child_language3_fluency": pl.Int8,
        "childgender": pl.Int8,
        "classroomtype": pl.Int8,
        "dominant_hand": pl.Int8,
        "guardian_maritalstatus": pl.Int8,
        "guardian_relationship___1": pl.Int8,
        "iep": pl.Int8,
        "infanttemp_adapt": pl.Int8,
        "infanttemp1": pl.Int8,
        "language_spoken": pl.Int8,
        "opt_delivery": pl.Int8,
        "residing_number": pl.Int8,
        "pronouns": pl.Int8,
        "schooltype": pl.Int8,
    }

    faulty_people_in_home = 2
    for index in range(1, 11):
        dtypes[f"peopleinhome{index}_relation"] = pl.Int8
        if index != faulty_people_in_home:
            dtypes[f"peopleinhome{index}_relationship"] = pl.Int8
        else:
            dtypes["peopleinhome_relationship"] = pl.Int8

    for index in range(1, 13):
        dtypes[f"guardian_relationship___{index}"] = pl.Int8

    return pl.read_csv(io.StringIO(csv_data), dtypes=dtypes, infer_schema_length=0)
