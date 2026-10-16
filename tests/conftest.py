"""Fixtures for climate_template tests."""

from pathlib import Path
from unittest.mock import patch

import custom_components
import pytest

# The test plugin may preload another `custom_components`; make ours visible.
_REPO_CC = str(Path(__file__).parent.parent / "custom_components")
if _REPO_CC not in custom_components.__path__:
    custom_components.__path__.append(_REPO_CC)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable loading of custom integrations in all tests."""
    yield


@pytest.fixture(autouse=True)
def no_generated_files():
    """Keep the integration from writing icons/translations into the source tree."""
    import custom_components.climate_template  # noqa: F401

    with patch(
        "custom_components.climate_template._generate_icons_and_translations"
    ):
        yield
