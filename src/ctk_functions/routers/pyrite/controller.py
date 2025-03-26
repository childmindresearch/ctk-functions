"""Business logic for the Pyrite endpoints."""

import io
import pathlib

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

    def _get_participant(self) -> models.CmiHbnIdTrack:
        """Fetches the participant's data from the SQL database.

        Returns:
            A row from the CMI_HB_IDTrack_t table.
        """
        logger.debug("Fetching participant %s.", self._mrn)
        with client.get_session() as session:
            participant = session.execute(
                sqlalchemy.select(models.CmiHbnIdTrack).where(
                    models.CmiHbnIdTrack.MRN == self._mrn,
                ),
            ).scalar_one_or_none()

        if not participant:
            raise fastapi.HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MRN not found.",
            )

        return participant

    def create(self) -> None:
        """Creates the Pyrite report."""
        self.document.add_heading("General Intellectual Function", level=1)
        wisc_composite.WiscCompositeTable(mrn=self._mrn).add_to(self.document)
        wisc_subtest.WiscSubtestTable(mrn=self._mrn).add_to(self.document)

        grooved_pegboard.GroovedPegboardTable(mrn=self._mrn).add_to(self.document)
        academic_achievement.AcademicAchievementTable(mrn=self._mrn).add_to(
            self.document,
        )

        celf5.Celf5Table(mrn=self._mrn).add_to(self.document)
        language.LanguageTable(mrn=self._mrn).add_to(self.document)

        ctopp_2.Ctopp2Table(mrn=self._mrn).add_to(self.document)

        self.document.add_heading(
            "Social-Emotional and Behavioral Functioning Questionnaires",
            level=1,
        )
        self.document.add_heading(
            "General Emotional and Behavioral Functioning",
            level=2,
        )
        cbcl_ysr.CbclTable(mrn=self._mrn).add_to(self.document)
        cbcl_ysr.YsrTable(mrn=self._mrn).add_to(self.document)
        self.document.add_heading(
            "Attention Deficit-Hyperactivity Symptoms and Behaviors",
        )
        swan.SwanTable(mrn=self._mrn).add_to(self.document)
        conners3.Conners3Table(mrn=self._mrn).add_to(self.document)

        self.document.add_heading("Autism Spectrum Symptoms and Behaviors", level=2)
        scq.ScqTable(mrn=self._mrn).add_to(self.document)
        gars.GarsTable(mrn=self._mrn).add_to(self.document)
        srs.SrsTable(mrn=self._mrn).add_to(self.document)

        self.document.add_heading("Depression and Anxiety Symptoms", level=2)
        mfq.MfqTable(mrn=self._mrn).add_to(self.document)
        scared.ScaredTable(mrn=self._mrn).add_to(self.document)

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
