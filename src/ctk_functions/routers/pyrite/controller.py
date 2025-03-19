"""Business logic for the Pyrite endpoints."""

import enum
import io
import pathlib
from typing import Any

import cmi_docx
import docx
import fastapi
import sqlalchemy
from fastapi import status

from ctk_functions.core import config
from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import (
    academic_achievement,
    cbcl_ysr,
    celf5,
    conners3,
    ctopp_2,
    gars,
    grooved_pegboard,
    language,
    mfq,
    scared,
    scq,
    srs,
    swan,
    wisc_composite,
    wisc_subtest,
)

logger = config.get_logger()
settings = config.get_settings()

DATA_DIR = settings.DATA_DIR


class _RGB(enum.Enum):
    """Represents an RGB color code for specific sections."""

    BASIC = (0, 0, 0)


def get_pyrite_report(mrn: str) -> bytes:
    """Generates a Pyrite report for a given MRN.

    Args:
        mrn: The participant's identifier.

    Returns:
        The .docx file bytes.
    """
    logger.debug("Entered controller of get_pyrite_report.")
    report = PyriteReport(mrn)
    report.create()

    logger.debug("Successfully generated Pyrite report.")
    report.document.save("/Users/reinder.vosdewael/Desktop/pyrite_report.docx")
    out = io.BytesIO()
    report.document.save(out)
    return out.getvalue()


class PyriteReport:
    """Builder of the Pyrite reports.

    Pyrite reports contain the overall test
    """

    def __init__(self, mrn: str) -> None:
        """Initialize the Pyrite report.

        Args:
            mrn: The participant's unique identifier.
        """
        self._mrn = mrn
        self.document = docx.Document(str(DATA_DIR / "pyrite_template.docx"))
        self._participant = self._get_participant()

    def _get_participant(self) -> sqlalchemy.Row[tuple[Any, ...]]:
        """Fetches the participant's data from the SQL database.

        Returns:
            A row from the CMI_HB_IDTrack_t table.
        """
        logger.debug("Fetching participant %s.", self._mrn)
        with client.get_session() as session:
            participant = session.execute(
                sqlalchemy.select(models.t_CMI_HBN_IDTrack_t).where(
                    self._mrn == models.t_CMI_HBN_IDTrack_t.c.MRN,  # type: ignore[arg-type]
                ),
            ).fetchone()

        if not participant:
            raise fastapi.HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MRN not found.",
            )

        return participant

    def create(self) -> None:
        """Creates the Pyrite report."""
        assessment_classes = (
            wisc_composite.WiscComposite,
            wisc_subtest.WiscSubtest,
            grooved_pegboard.GroovedPegboard,
            academic_achievement.AcademicAchievement,
            celf5.Celf5,
            language.Language,
            ctopp_2.Ctopp2,
            cbcl_ysr.Cbcl,
            cbcl_ysr.Ysr,
            swan.Swan,
            conners3.Conners3,
            scq.Scq,
            gars.Gars,
            srs.Srs,
            mfq.Mfq,
            scared.Scared,
        )

        for assessment_class in assessment_classes:
            table = assessment_class(eid=self._participant.GUID)
            if table.data:
                table.add(self.document)
                self.document.add_paragraph()

        self._replace_participant_information()

    def _save(self, filepath: str | pathlib.Path) -> None:
        """Saves the report to a file.

        Used for dev testing only.

        Args:
            filepath: The filepath to save the report to.
        """
        if isinstance(filepath, pathlib.Path):
            filepath = str(filepath.expanduser())
        self.document.save(filepath)

    def _replace_participant_information(self) -> None:
        """Replaces the patient information in the report."""
        logger.debug("Replacing patient information in the report.")

        first_name = self._participant.first_name
        full_name = first_name + " " + self._participant.last_name
        first_name_possessive = first_name + ("'" if first_name.endswith("s") else "'s")
        replacements = {
            "full_name": full_name,
            "first_name_possessive": first_name_possessive,
        }

        for template, replacement in replacements.items():
            template_formatted = "{{" + template.upper() + "}}"
            cmi_docx.ExtendDocument(self.document).replace(
                template_formatted,
                replacement,
            )
