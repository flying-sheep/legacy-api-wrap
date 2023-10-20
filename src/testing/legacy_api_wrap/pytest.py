"""Pytest plugin for legacy_api_wrap."""

import sys
import warnings
from typing import Generator

import pytest

__all__ = ["_doctest_env", "pytest_itemcollected"]


@pytest.fixture()
def _doctest_env() -> Generator[None, None, None]:
    """Pytest fixture to make doctests not error on expected warnings."""
    sys.stderr, stderr_orig = sys.stdout, sys.stderr
    with warnings.catch_warnings():
        warnings.resetwarnings()  # reset -Werror
        warnings.filterwarnings("ignore", r"The specified parameters", DeprecationWarning)
        yield
    sys.stderr = stderr_orig


def pytest_itemcollected(item: pytest.Item) -> None:
    """Modify test items.

    See https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.hookspec.pytest_itemcollected
    """
    if isinstance(item, pytest.DoctestItem):
        item.add_marker(pytest.mark.usefixtures("_doctest_env"))
