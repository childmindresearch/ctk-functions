"""Tests for the Appendix A data structures."""

from typing import get_args

from ctk_functions.routers.pyrite import types
from ctk_functions.routers.pyrite.reports import appendix_a


def test_all_ids_in_manager() -> None:
    """Tests that all TestIds appear in the manager."""
    manager = appendix_a.TestDescriptionManager
    ids = get_args(types.TestId)
    manager_ids = manager.__dict__.keys()

    # __dict__ provides pydantic attributes too, so test for subset rather
    # than equality.
    assert set(ids).issubset(manager_ids)
