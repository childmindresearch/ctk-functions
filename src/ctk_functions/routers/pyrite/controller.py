"""Business logic for the Pyrite endpoints."""

import io
from collections.abc import Callable
from typing import Self, get_type_hints

import cmi_docx
import docx
import fastapi
import pydantic
from docx import document
from fastapi import status

from ctk_functions.core import config
from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import (
    academic_achievement,
    base,
    cbcl_ysr,
    celf5,
    conners3,
    ctopp2,
    gars,
    grooved_pegboard,
    language,
    mfq,
    scared,
    scq,
    srs,
    swan,
    utils,
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


class ReportSection(pydantic.BaseModel):
    """Represents a section in the report structure."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    title: str | None = None
    level: int | None = None
    condition: Callable[[], bool] = lambda: True
    tables: list[base.WordTableSection] = pydantic.Field(default_factory=list)
    subsections: list[Self] = pydantic.Field(default_factory=list)

    def add_to(self, doc: document.Document) -> None:
        """Adds the section to a document.

        Args:
            doc: The document to add the section to.
        """
        if not self.condition():
            return
        if self.title and self.level:
            doc.add_heading(self.title, level=self.level)
        for table in self.tables:
            if table.is_available():
                table.add_to(doc)
        for subsection in self.subsections:
            subsection.add_to(doc)


@pydantic.dataclasses.dataclass(
    config=pydantic.ConfigDict(arbitrary_types_allowed=True),
)
class PyriteTableCollection:
    """Collection of all tables used in Pyrite reports."""

    mrn: str

    # Tables must start with "tbl_"
    tbl_wisc_composite: wisc_composite.WiscCompositeTable = pydantic.Field(init=False)
    tbl_wisc_subtest: wisc_subtest.WiscSubtestTable = pydantic.Field(init=False)
    tbl_grooved_pegboard: grooved_pegboard.GroovedPegboardTable = pydantic.Field(
        init=False,
    )
    tbl_academic_achievement: academic_achievement.AcademicAchievementTable = (
        pydantic.Field(init=False)
    )
    tbl_celf5: celf5.Celf5Table = pydantic.Field(init=False)
    tbl_language: language.LanguageTable = pydantic.Field(init=False)
    tbl_ctopp2: ctopp2.Ctopp2Table = pydantic.Field(init=False)
    tbl_cbcl: cbcl_ysr.CbclTable = pydantic.Field(init=False)
    tbl_ysr: cbcl_ysr.YsrTable = pydantic.Field(init=False)
    tbl_swan: swan.SwanTable = pydantic.Field(init=False)
    tbl_conners3: conners3.Conners3Table = pydantic.Field(init=False)
    tbl_scq: scq.ScqTable = pydantic.Field(init=False)
    tbl_gars: gars.GarsTable = pydantic.Field(init=False)
    tbl_srs: srs.SrsTable = pydantic.Field(init=False)
    tbl_mfq: mfq.MfqTable = pydantic.Field(init=False)
    tbl_scared: scared.ScaredTable = pydantic.Field(init=False)

    def __post_init__(self) -> None:
        """Populates all tables with their instance."""
        hints = get_type_hints(self)
        for field_name, field_type in hints.items():
            if field_name.startswith("tbl_") and issubclass(
                field_type,
                base.WordTableSection,
            ):
                setattr(self, field_name, field_type(self.mrn))


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
        self._tables = PyriteTableCollection(mrn=mrn)
        self.document = docx.Document(str(DATA_DIR / "pyrite_template.docx"))
        self._participant = self._get_participant()

    def create(self) -> None:
        """Creates the Pyrite report."""
        structure = self._report_structure()
        for section in structure:
            section.add_to(self.document)
        self._replace_participant_information()

    def _get_participant(self) -> models.CmiHbnIdTrack:
        """Fetches the participant's data from the SQL database.

        Returns:
            A row from the CMI_HB_IDTrack_t table.
        """
        logger.debug("Fetching participant %s.", self._mrn)
        try:
            return utils.fetch_participant_row("MRN", self._mrn, models.CmiHbnIdTrack)  # type: ignore[no-any-return, unused-ignore] # Getting errors both when no-any-return is, and is not used.
        except utils.TableDataNotFoundError as exception_info:
            raise fastapi.HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MRN not found.",
            ) from exception_info

    def _replace_participant_information(self) -> None:
        """Replaces the patient information in the report."""
        logger.debug("Replacing patient information in the report.")

        first_name = self._participant.first_name
        full_name = f"{first_name} {self._participant.last_name}"
        first_name_possessive = (
            f"{first_name}{"'" if first_name.endswith('s') else "'s"}"
        )
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

    def _report_structure(self) -> list[ReportSection]:
        """Creates the structure of the Pyrite report.

        Returns:
            The structure of the Pyrite report, containing only available sections.
        """

        def is_any_available(*tbls: base.WordTableSection) -> bool:
            return any(tbl.is_available() for tbl in tbls)

        def is_all_available(*tbls: base.WordTableSection) -> bool:
            return all(tbl.is_available() for tbl in tbls)

        tables = self._tables  # Alias because this is used a LOT.

        return [
            ReportSection(
                title="General Intellectual Function",
                level=1,
                tables=[],
                condition=lambda: is_all_available(
                    tables.tbl_wisc_composite, tables.tbl_wisc_subtest
                ),
                subsections=[
                    ReportSection(
                        title=(
                            "The Wechsler Intelligence Scale for Children-Fifth "
                            "Edition (WISC-V)"
                        ),
                        level=2,
                        tables=[],
                    ),
                    ReportSection(
                        title=None,
                        level=None,
                        tables=[tables.tbl_wisc_composite],
                    ),
                    ReportSection(
                        title=None,
                        level=None,
                        tables=[tables.tbl_wisc_subtest],
                    ),
                ],
            ),
            ReportSection(
                title="Abbreviated Neurocognitive Assessment",
                level=2,
                tables=[tables.tbl_grooved_pegboard],
                condition=lambda: tables.tbl_grooved_pegboard.is_available(),
            ),
            ReportSection(
                title="Academic Achievement",
                level=1,
                tables=[tables.tbl_academic_achievement],
                condition=lambda: tables.tbl_academic_achievement.is_available(),
            ),
            ReportSection(
                title="Language Skills",
                level=1,
                tables=[tables.tbl_celf5, tables.tbl_language, tables.tbl_ctopp2],
                condition=lambda: is_any_available(
                    tables.tbl_celf5,
                    tables.tbl_language,
                    tables.tbl_ctopp2,
                ),
            ),
            ReportSection(
                title="Social-Emotional and Behavioral Functioning Questionnaires",
                level=1,
                tables=[],
                condition=lambda: is_any_available(
                    tables.tbl_cbcl,
                    tables.tbl_ysr,
                    tables.tbl_swan,
                    tables.tbl_conners3,
                    tables.tbl_scq,
                    tables.tbl_gars,
                    tables.tbl_srs,
                    tables.tbl_mfq,
                    tables.tbl_scared,
                ),
                subsections=[
                    ReportSection(
                        title="General Emotional and Behavioral Functioning",
                        level=2,
                        tables=[],
                        condition=lambda: is_any_available(
                            tables.tbl_cbcl,
                            tables.tbl_ysr,
                        ),
                        subsections=[
                            ReportSection(
                                title=(
                                    "Child Behavior Checklist - Parent Report "
                                    "Form (CBCL)"
                                ),
                                level=2,
                                tables=[tables.tbl_cbcl],
                                condition=lambda: tables.tbl_cbcl.is_available(),
                            ),
                            ReportSection(
                                title=(
                                    "Child Behavior Checklist - Youth Self Report (YSR)"
                                ),
                                level=2,
                                tables=[tables.tbl_ysr],
                                condition=lambda: tables.tbl_ysr.is_available(),
                            ),
                        ],
                    ),
                    ReportSection(
                        title="Attention Deficit-Hyperactivity Symptoms and Behaviors",
                        level=2,
                        tables=[],
                        condition=lambda: is_any_available(
                            tables.tbl_swan,
                            tables.tbl_conners3,
                        ),
                        subsections=[
                            ReportSection(
                                title=(
                                    "Strengths and Weaknesses of ADHD Symptoms "
                                    "and Normal Behavior (SWAN)"
                                ),
                                level=2,
                                tables=[tables.tbl_swan],
                                condition=lambda: tables.tbl_swan.is_available(),
                            ),
                            ReportSection(
                                title="Conners 3 - Child Short Form",
                                level=2,
                                tables=[tables.tbl_conners3],
                                condition=lambda: tables.tbl_conners3.is_available(),
                            ),
                        ],
                    ),
                    ReportSection(
                        title="Autism Spectrum Symptoms and Behaviors",
                        level=2,
                        tables=[],
                        condition=lambda: is_any_available(
                            tables.tbl_scq,
                            tables.tbl_gars,
                            tables.tbl_srs,
                        ),
                        subsections=[
                            ReportSection(
                                title="Social Communication Questionnaire",
                                level=2,
                                tables=[tables.tbl_scq],
                                condition=lambda: tables.tbl_scq.is_available(),
                            ),
                            ReportSection(
                                title=(
                                    "Gilliam Autism Rating Scale, Third Edition "
                                    "(GARS-3)"
                                ),
                                level=2,
                                tables=[tables.tbl_gars],
                                condition=lambda: tables.tbl_gars.is_available(),
                            ),
                            ReportSection(
                                title="Social Responsiveness Scale",
                                level=2,
                                tables=[tables.tbl_scq],
                                condition=lambda: tables.tbl_scq.is_available(),
                            ),
                        ],
                    ),
                    ReportSection(
                        title="Depression and Anxiety Symptoms",
                        level=2,
                        tables=[],
                        condition=lambda: is_any_available(
                            tables.tbl_mfq,
                            tables.tbl_scared,
                        ),
                        subsections=[
                            ReportSection(
                                title=(
                                    "Mood and Feelings Questionnaire (MFQ) "
                                    "- Long Version"
                                ),
                                level=2,
                                tables=[tables.tbl_mfq],
                                condition=lambda: tables.tbl_mfq.is_available(),
                            ),
                            ReportSection(
                                title="Screen for Child Anxiety Related Disorders",
                                level=2,
                                tables=[tables.tbl_scared],
                                condition=lambda: tables.tbl_scared.is_available(),
                            ),
                        ],
                    ),
                ],
            ),
        ]
