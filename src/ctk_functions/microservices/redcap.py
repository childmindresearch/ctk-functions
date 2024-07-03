"""This module contains functions for interacting with REDcap."""

import io
import re
from typing import Any

import polars as pl
import redcap

from ctk_functions import config, exceptions

settings = config.get_settings()
REDCAP_ENDPOINT = settings.REDCAP_ENDPOINT
REDCAP_API_TOKEN = settings.REDCAP_API_TOKEN

logger = config.get_logger()


def get_intake_data(mrn: str) -> dict[str, Any]:
    """Gets the intake data from REDcap.

    REDCap does not allow filtering by redcap_survey_identifier, so we have to
    download all records, find the associated record_id, and then filter by that.

    REDCap survey identifiers occasionally get strings appended. We search only for
    five consecutive numbers.


    Args:
        mrn: The patient's MRN (unique identifier).

    Returns:
        The intake data for the survey.
    """
    if not re.match(r"^\d{5}$", mrn):
        raise exceptions.RedcapException("MRN must be five consecutive numbers.")

    logger.debug(f"Getting intake data for MRN {mrn}.")
    project = redcap.Project(str(REDCAP_ENDPOINT), REDCAP_API_TOKEN.get_secret_value())  # type: ignore
    redcap_fields = project.export_records(
        format_type="csv",
        fields=["firstname"],
        export_survey_fields=True,
        raw_or_label="label",
    )

    redcap_fields = pl.read_csv(io.StringIO(redcap_fields), infer_schema_length=0)
    record_ids = redcap_fields.filter(
        pl.col("redcap_survey_identifier").str.contains(mrn)
    )["record_id"]

    if len(record_ids) == 0:
        raise exceptions.RedcapException("No record found for the given MRN.")

    patient_data = project.export_records(
        format_type="csv",
        export_survey_fields=True,
        records=[record_ids[0]],
    )

    return parse_redcap_dtypes(patient_data)


def parse_redcap_dtypes(csv_data: str) -> dict[str, Any]:
    """Parses the REDcap data with the appropriate data types.

    REDCap data types are finnicky due to the large number of freeform string inputs and
    the .csv format. This function parses the data with the appropriate data types.
    All data that isn't explicitly typed by this function is set to a string.

    Args:
        csv_data: The CSV data to parse.

    Returns:
        The parsed REDcap data.
    """
    logger.debug("Parsing REDcap data with appropriate data types.")
    dtypes = {
        "age": pl.Float32,
        "biohx_dad_other": pl.Int8,
        "biohx_mom_other": pl.Int8,
        "birth_location": pl.Int8,
        "child_glasses": pl.Int8,
        "child_hearing_aid": pl.Int8,
        "child_language1_fluency": pl.Int8,
        "child_language2_fluency": pl.Int8,
        "child_language3_fluency": pl.Int8,
        "childgender": pl.Int8,
        "classroomtype": pl.Int8,
        "current_grades": pl.Int8,
        "dominant_hand": pl.Int8,
        "guardian_maritalstatus": pl.Int8,
        "guardian_relationship___1": pl.Int8,
        "iep": pl.Int8,
        "infanttemp_adapt": pl.Int8,
        "infanttemp1": pl.Int8,
        "language_spoken": pl.Int8,
        "opt_delivery": pl.Int8,
        "peer_relations": pl.Int8,
        "recent_academicperformance": pl.Int8,
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

    dataframe = pl.read_csv(
        io.StringIO(csv_data), schema_overrides=dtypes, infer_schema_length=0
    )
    if dataframe.is_empty() or dataframe.shape[0] == 0:
        raise exceptions.RedcapException("No data found for the given MRN.")

    if dataframe.shape[0] > 1:
        raise exceptions.RedcapException("Multiple records found for the given MRN.")

    return dataframe.row(0, named=True)
