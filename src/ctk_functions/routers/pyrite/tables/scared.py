"""Module for getting the Scared table."""

import functools

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base
from ctk_functions.routers.pyrite.tables.generic import parent_child

SCARED_ROW_LABELS = (
    parent_child.ParentChildRow(
        subscale="Panic Disorder/Sig. Somatic Symptoms",
        parent_column="SCARED_P_PN",
        child_column="SCARED_SR_PN",
        relevance=[
            base.ClinicalRelevance(
                low=6,
                high=None,
                label=None,
                style=cmi_docx.TableStyle(
                    cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
                ),
            ),
        ],
    ),
    parent_child.ParentChildRow(
        subscale="Generalized Anxiety Disorder",
        parent_column="SCARED_P_GD",
        child_column="SCARED_SR_GD",
        relevance=[
            base.ClinicalRelevance(
                low=8,
                high=None,
                label=None,
                style=cmi_docx.TableStyle(
                    cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
                ),
            ),
        ],
    ),
    parent_child.ParentChildRow(
        subscale="Separation Anxiety Disorder",
        parent_column="SCARED_P_SP",
        child_column="SCARED_SR_SP",
        relevance=[
            base.ClinicalRelevance(
                low=4,
                high=None,
                label=None,
                style=cmi_docx.TableStyle(
                    cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
                ),
            ),
        ],
    ),
    parent_child.ParentChildRow(
        subscale="Social Anxiety Disorder",
        parent_column="SCARED_P_SC",
        child_column="SCARED_SR_SC",
        relevance=[
            base.ClinicalRelevance(
                low=7,
                high=None,
                label=None,
                style=cmi_docx.TableStyle(
                    cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
                ),
            ),
        ],
    ),
    parent_child.ParentChildRow(
        subscale="Significant School Avoidance",
        parent_column="SCARED_P_SH",
        child_column="SCARED_SR_SH",
        relevance=[
            base.ClinicalRelevance(
                low=2,
                high=None,
                label=None,
                style=cmi_docx.TableStyle(
                    cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
                ),
            ),
        ],
    ),
    parent_child.ParentChildRow(
        subscale="Total Score: Anxiety Disorder",
        parent_column="SCARED_P_Total",
        child_column="SCARED_SR_Total",
        relevance=[
            base.ClinicalRelevance(
                low=24,
                high=None,
                label=None,
                style=cmi_docx.TableStyle(
                    cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
                ),
            ),
        ],
    ),
)


class ScaredDataSource(base.DataProducer):
    """Fetches the data for the Scared table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches the Scared data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        return parent_child.build_parent_child_table(
            mrn,
            models.ScaredParent,
            models.ScaredSelf,
            SCARED_ROW_LABELS,
        )


class ScaredTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the Scared table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Scared renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = ScaredDataSource
