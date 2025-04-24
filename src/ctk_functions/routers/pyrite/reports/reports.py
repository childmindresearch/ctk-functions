"""Contains definitions of Pyrite report formats."""

from collections.abc import Iterable
from typing import Literal, TypeVar

from ctk_functions.routers.pyrite import types
from ctk_functions.routers.pyrite.reports import appendix_a, introduction, sections
from ctk_functions.routers.pyrite.tables import (
    academic_achievement,
    base,
    cbc,
    celf5,
    conners3,
    ctopp2,
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

T = TypeVar("T")
VERSIONS = Literal["alabaster"]


class _PyriteTableCollection:
    """Collection of all tables used in Pyrite reports."""

    def __init__(self, mrn: str) -> None:
        """Initializes all tables."""
        self.asr = cbc.AsrTable(mrn)
        self.academic_achievement = academic_achievement.AcademicAchievementTable(mrn)
        self.cbcl = cbc.CbclTable(mrn)
        self.celf5 = celf5.Celf5Table(mrn)
        self.conners3 = conners3.Conners3Table(mrn)
        self.ctopp2 = ctopp2.Ctopp2Table(mrn)
        self.grooved_pegboard = grooved_pegboard.GroovedPegboardTable(mrn)
        self.language = language.LanguageTable(mrn)
        self.mfq = mfq.MfqTable(mrn)
        self.scared = scared.ScaredTable(mrn)
        self.scq = scq.ScqTable(mrn)
        self.srs = srs.SrsTable(mrn)
        self.swan = swan.SwanTable(mrn)
        self.trf = cbc.TrfTable(mrn)
        self.wisc_composite = wisc_composite.WiscCompositeTable(mrn)
        self.wisc_subtest = wisc_subtest.WiscSubtestTable(mrn)
        self.ysr = cbc.YsrTable(mrn)


def get_report_structure(
    mrn: str,
    version: VERSIONS,
) -> tuple[sections.Section, ...]:
    """Fetches a report structure based on version name.

    Valid versions are:
        alabaster: Maintained from 2025-04-02 until the present. This version
            outputs all available tables and is currently the 'main' version.
        chalk: Debug version that runs requested tables only.

    Args:
        mrn: The participant's unique identifier.
        version: The report version name.

    Returns:
          The structure of the Pyrite report.
    """
    if version == "alabaster":
        return _report_alabaster(mrn)
    msg = f"Invalid Pyrite version: {version}."
    raise ValueError(msg)


def _report_alabaster(mrn: str) -> tuple[sections.Section, ...]:
    """Creates the structure of the 2024-04-02 Pyrite report.

    Args:
        mrn: The participant's unique identifier.

    Returns:
        The structure of the Pyrite report, containing only available sections.
    """
    tables = _PyriteTableCollection(mrn)
    table_sections = _get_alabaster_table_structure(tables)
    test_ids = _tables_to_test_ids(mrn, table_sections)
    intro = introduction.test_ids_to_introduction(mrn, test_ids)
    appendix = appendix_a.test_ids_to_appendix_a(test_ids)
    return (
        *intro,
        sections.PageBreak(),
        *appendix,
        sections.PageBreak(),
        *table_sections,
    )


def _tables_to_test_ids(
    mrn: str, table_sections: Iterable[sections.Section]
) -> list[types.TestId]:
    """Converts tables to the test_ids that they use.

    Args:
        mrn: The participant's unique identifier.
        table_sections: The list of sections to extract IDs from.

    Returns:
        Unique test IDs sorted alphabetically.
    """
    used_producers = _extract_producers_used(table_sections)
    available_producers = [
        producer for producer in used_producers if producer.is_available(mrn)
    ]
    test_ids: list[types.TestId] = _flatten(
        [tbl.test_ids(mrn) for tbl in available_producers]
    )
    return sorted(dict.fromkeys(test_ids))


def _extract_producers_used(
    structure: Iterable[sections.Section],
) -> tuple[type[base.DataProducer], ...]:
    """Extracts the data producers used in sections."""
    producers = []
    for section in structure:
        section_tables: list[base.WordTableSection] = getattr(section, "tables", [])
        producers.extend([tbl.data_source for tbl in section_tables])
        producers.extend(_extract_producers_used(section.subsections))
    return tuple(producers)


def _get_alabaster_table_structure(
    tables: _PyriteTableCollection,
) -> tuple[sections.Section, ...]:
    """Defines the structure of the Alabaster tables."""
    return (
        sections.ParagraphSection(
            content="Results Appendix", style="Heading 1 Centered"
        ),
        sections.ParagraphSection(
            content="General Intellectual Function",
            style="Heading 1",
            condition=lambda: _all_tables_available(
                tables.wisc_composite, tables.wisc_subtest
            ),
            subsections=[
                sections.TableSection(
                    title=(
                        "The Wechsler Intelligence Scale for Children-Fifth "
                        "Edition (WISC-V)"
                    ),
                    level=3,
                    tables=[tables.wisc_composite, tables.wisc_subtest],
                ),
            ],
        ),
        sections.ParagraphSection(
            content="Fine Motor Dexterity",
            style="Heading 1",
            condition=lambda: tables.grooved_pegboard.is_available(),
            subsections=[
                sections.TableSection(
                    title="Lafayette Grooved Pegboard Test",
                    level=3,
                    tables=[tables.grooved_pegboard],
                )
            ],
        ),
        sections.PageBreak(),
        sections.TableSection(
            title="Academic Achievement",
            level=1,
            tables=[tables.academic_achievement],
            condition=lambda: tables.academic_achievement.is_available(),
        ),
        sections.PageBreak(),
        sections.TableSection(
            title="Language Skills",
            level=1,
            tables=[tables.celf5, tables.language, tables.ctopp2],
            condition=lambda: _any_table_available(
                tables.celf5,
                tables.language,
                tables.ctopp2,
            ),
        ),
        sections.PageBreak(),
        sections.ParagraphSection(
            content="Social-Emotional and Behavioral Functioning Questionnaires",
            style="Heading 1 Centered",
            condition=lambda: _any_table_available(
                tables.cbcl,
                tables.ysr,
                tables.swan,
                tables.conners3,
                tables.scq,
                tables.srs,
                tables.mfq,
                tables.scared,
            ),
            subsections=[
                sections.TableSection(
                    title="Child Behavior Checklist - Parent Report Form (CBCL)",
                    level=3,
                    tables=[tables.cbcl],
                    condition=lambda: tables.cbcl.is_available(),
                ),
                sections.TableSection(
                    title="Child Behavior Checklist - Youth Self Report (YSR)",
                    level=3,
                    tables=[tables.ysr],
                    condition=lambda: tables.ysr.is_available(),
                ),
                sections.TableSection(
                    title="Child Behavior Checklist - Teacher Report Form (TRF)",
                    level=3,
                    tables=[tables.trf],
                    condition=lambda: tables.trf.is_available(),
                ),
                sections.TableSection(
                    title="Child Behavior Checklist - Adult Self Report Form (ASR)",
                    level=3,
                    tables=[tables.asr],
                    condition=lambda: tables.asr.is_available(),
                ),
                sections.ParagraphSection(
                    content="Attention Deficit-Hyperactivity Symptoms and Behaviors",
                    style="Heading 1",
                    condition=lambda: _any_table_available(
                        tables.swan,
                        tables.conners3,
                    ),
                    subsections=[
                        sections.TableSection(
                            title=(
                                "Strengths and Weaknesses of ADHD Symptoms "
                                "and Normal Behavior (SWAN)"
                            ),
                            level=3,
                            tables=[tables.swan],
                            condition=lambda: tables.swan.is_available(),
                        ),
                        sections.TableSection(
                            title="Conners 3 - Child Short Form",
                            level=3,
                            tables=[tables.conners3],
                            condition=lambda: tables.conners3.is_available(),
                        ),
                    ],
                ),
                sections.ParagraphSection(
                    content="Autism Spectrum Symptoms and Behaviors",
                    style="Heading 1",
                    condition=lambda: _any_table_available(
                        tables.scq,
                        tables.srs,
                    ),
                    subsections=[
                        sections.TableSection(
                            title="Social Communication Questionnaire",
                            level=3,
                            tables=[tables.scq],
                            condition=lambda: tables.scq.is_available(),
                        ),
                        sections.TableSection(
                            title="Social Responsiveness Scale",
                            level=3,
                            tables=[tables.srs],
                            condition=lambda: tables.srs.is_available(),
                        ),
                    ],
                ),
                sections.PageBreak(),
                sections.ParagraphSection(
                    content="Depression and Anxiety Symptoms",
                    style="Heading 1",
                    condition=lambda: _any_table_available(
                        tables.mfq,
                        tables.scared,
                    ),
                    subsections=[
                        sections.TableSection(
                            title=(
                                "Mood and Feelings Questionnaire (MFQ) - Long Version"
                            ),
                            level=3,
                            tables=[tables.mfq],
                            condition=lambda: tables.mfq.is_available(),
                        ),
                        sections.TableSection(
                            title="Screen for Child Anxiety Related Disorders",
                            level=3,
                            tables=[tables.scared],
                            condition=lambda: tables.scared.is_available(),
                        ),
                    ],
                ),
            ],
        ),
    )


def _any_table_available(*tbls: base.WordTableSection) -> bool:
    """True if any table's data is available, false otherwise."""
    return any(tbl.is_available() for tbl in tbls)


def _all_tables_available(*tbls: base.WordTableSection) -> bool:
    """True if all tables' data are available, false otherwise."""
    return all(tbl.is_available() for tbl in tbls)


def _flatten(collection: Iterable[Iterable[T]]) -> list[T]:
    """Flattens an iterable of iterables into a flat list."""
    return [item for sub_iterable in collection for item in sub_iterable]
