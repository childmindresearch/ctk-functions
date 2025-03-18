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
    grooved_pegboard,
    scq,
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


class ParticipantTables:
    """A dataclass representing a participant's assessment data.

    This class aggregates various assessment data for a participant by their EID.
    """

    def __init__(self, eid: str) -> None:
        """Initialize all assessment objects with the participant's EID."""
        self.eid = eid
        self.academic_achievement = academic_achievement.AcademicAchievement(
            eid=self.eid,
        )
        self.cbcl = cbcl_ysr.Cbcl(eid=self.eid)
        self.conners3 = conners3.Conners3(eid=self.eid)
        self.ysr = cbcl_ysr.Ysr(eid=self.eid)
        self.celf5 = celf5.Celf5(eid=self.eid)
        self.ctopp2 = ctopp_2.Ctopp2(eid=self.eid)
        self.grooved_pegboard = grooved_pegboard.GroovedPegboard(eid=self.eid)
        self.scq = scq.Scq(eid=self.eid)
        self.swan = swan.Swan(eid=self.eid)
        self.wisc_composite = wisc_composite.WiscComposite(eid=self.eid)
        self.wisc_subtest = wisc_subtest.WiscSubtest(eid=self.eid)


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
        self._tables = ParticipantTables(eid=self._participant.GUID)

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

    def create(self) -> None:  # noqa: C901
        """Creates the Pyrite report."""
        if self._tables.wisc_composite.data:  # type: ignore[truthy-function]
            # Check only data of one table as they use the same data
            self.document.add_heading(
                "The Wechsler Intelligence Scale for Children-Fifth Edition (WISC-V)",
                level=1,
            )
            self._tables.wisc_composite.add(self.document)
            self.document.add_paragraph()
            self._tables.wisc_subtest.add(self.document)
            self.document.add_paragraph()

        if self._tables.grooved_pegboard.data:  # type: ignore[truthy-function]
            self.document.add_heading(
                text="Abbreviated Neurocognitive Assessment",
                level=1,
            )
            self._tables.grooved_pegboard.add(self.document)
            self.document.add_paragraph()

        if self._tables.academic_achievement.data:  # type: ignore[truthy-function]
            self.document.add_heading(
                text="Academic Achievement",
                level=1,
            )
            self._tables.academic_achievement.add(self.document)
            self.document.add_paragraph()

        if self._tables.celf5.data:  # type: ignore[truthy-function]
            self.document.add_heading(
                text="Language Screening",
                level=1,
            )
            self._tables.celf5.add(self.document)
            self.document.add_paragraph()

        if self._tables.ctopp2.data:  # type: ignore[truthy-function]
            self._tables.ctopp2.add(self.document)
            self.document.add_paragraph()

        if self._tables.cbcl.data:  # type: ignore[truthy-function]
            self.document.add_heading(
                text="Child Behavior Checklist - Parent Report Form (CBCL)",
                level=1,
            )
            self._tables.cbcl.add(self.document)
            self.document.add_paragraph()

        if self._tables.ysr.data:  # type: ignore[truthy-function]
            self.document.add_heading(
                text="Child Behavior Checklist - Youth Self Report (YSR)",
                level=1,
            )
            self._tables.ysr.add(self.document)
            self.document.add_paragraph()
        if self._tables.swan.data:  # type: ignore[truthy-function]
            self.document.add_heading(
                "Strengths and Weaknesses of ADHD Symptoms and Normal Behavior (SWAN)",
                level=1,
            )
            self._tables.swan.add(self.document)
            self.document.add_paragraph()
        if self._tables.conners3.data:  # type: ignore[truthy-function]
            self.document.add_heading(
                "Conners 3 - Child Short Form",
                level=1,
            )
            self._tables.conners3.add(self.document)
            self.document.add_paragraph()
        if self._tables.scq.data:  # type: ignore[truthy-function]
            self.document.add_heading(
                text="Social Communication Questionnaire",
                level=1,
            )
            self._tables.scq.add(self.document)
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
