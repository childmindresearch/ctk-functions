"""Business logic for the Pyrite endpoints."""

import io

import docx

from ctk_functions.core import config
from ctk_functions.routers.pyrite.tables import base

logger = config.get_logger()
settings = config.get_settings()

DATA_DIR = settings.DATA_DIR


def post_referral(table: tuple[tuple[str, ...], ...]) -> bytes:
    """Generates a referral for a given table.

    Args:
        table: Array of an array of strings representing a table, outer array
            represents rows, the inner array cells.

    Returns:
        The .docx file bytes.
    """
    doc = docx.Document(str(DATA_DIR / "referral_template.docx"))
    rows = [[base.WordTableCell(content=text) for text in row] for row in table]
    markup = base.WordTableMarkup(rows=rows)
    renderer = base.WordDocumentTableRenderer(markup=markup)
    renderer.add_to(doc)

    out = io.BytesIO()
    doc.save(out)
    doc.save("/Users/reinder.vosdewael/Desktop/test.docx")
    return out.getvalue()
