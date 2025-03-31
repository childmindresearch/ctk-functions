"""Module for inserting the CBCL and YSR tables."""

import functools

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils
from ctk_functions.routers.pyrite.tables.generic import tscore

# There are two sets of thresholds for clinical relevance.
# The one with higher scores is denoted as "HIGH", the other as "LOW".
CLINICAL_RELEVANCE_HIGH = [
    base.ClinicalRelevance(
        low=None,
        high=65,
        high_inclusive=False,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    base.ClinicalRelevance(
        low=65,
        high=70,
        low_inclusive=True,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=70,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]

CLINICAL_RELEVANCE_LOW = [
    base.ClinicalRelevance(
        low=None,
        high=60,
        high_inclusive=False,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    base.ClinicalRelevance(
        low=60,
        high=65,
        low_inclusive=True,
        label="borderline range",
        style=cmi_docx.TableStyle(paragraph=cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=65,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            paragraph=cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]


# Defines the rows and their order of appearance.
CBCL_YSR_ROW_LABELS = {
    key: (
        tscore.TScoreRowLabel(
            subscale="Anxious/Depressed",
            score_column=f"{key}_AD_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Withdrawn/Depressed",
            score_column=f"{key}_WD_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Somatic Complaints",
            score_column=f"{key}_SC_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Social Problems",
            score_column=f"{key}_SP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Thought Problems",
            score_column=f"{key}_TP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Attention Problems",
            score_column=f"{key}_AP_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Rule Breaking Behaviors",
            score_column=f"{key}_RBB_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Aggressive Behaviors",
            score_column=f"{key}_AB_T",
            relevance=CLINICAL_RELEVANCE_HIGH,
        ),
        tscore.TScoreRowLabel(
            subscale="Internalizing (Emotional) Problems",
            score_column=f"{key}_Int_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
        tscore.TScoreRowLabel(
            subscale="Externalizing (Behavioral) Problems",
            score_column=f"{key}_Ext_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
        tscore.TScoreRowLabel(
            subscale="Total Problems",
            score_column=f"{key}_Total_T",
            relevance=CLINICAL_RELEVANCE_LOW,
        ),
    )
    for key in ("CBCL", "YSR")
}


class CbclDataSource(base.DataProducer):
    """Fetches the data for the CBCL table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches CBCL data for the given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Cbcl)
        return tscore.build_tscore_table(data, CBCL_YSR_ROW_LABELS["CBCL"])


class CbclTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the CBCL table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the CBCL renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = CbclDataSource


class YsrDataSource(base.DataProducer):
    """Fetches the data for the YSR table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches YSR data for the given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Ysr)
        return tscore.build_tscore_table(data, CBCL_YSR_ROW_LABELS["YSR"])


class YsrTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the YSR table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the YSR renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.data_source = YsrDataSource
