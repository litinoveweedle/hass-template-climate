"""The climate template component."""

import json
import logging
from pathlib import Path

from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN

from .climate import CONF_ICONS, DOMAIN, derive_translation_key

_LOGGER = logging.getLogger(__name__)

ICONS_PATH = Path(__file__).parent / "icons.json"


async def async_setup(hass, config):
    """Set up the climate_template component.
    This has no work to do itself (entities are set up per-platform via
    async_setup_platform in climate.py), but defining it is what makes
    Home Assistant register "climate_template" under its own bare domain
    in hass.config.components. Without this hook, a YAML `platform:`
    integration like this one only ever gets registered as the dotted
    "climate_template.climate" form -- and the frontend's icon-translation
    lookup (isComponentLoaded) checks for the bare domain name, so it
    silently never requests icons.json without this.
    """
    await hass.async_add_executor_job(_generate_icons, config)
    return True


def _generate_icons(config):
    """Regenerate icons.json from each entity's `icons` YAML option.

    Config validation has already turned every "platform: climate_template"
    block under "climate:" into a dict shaped by PLATFORM_SCHEMA (this runs
    before any component's async_setup), so we can read it straight from the
    raw config instead of waiting on per-entity async_setup_platform calls.
    Entities without a derivable identifier (see `derive_translation_key`) or
    without `icons` are skipped, keeping the feature fully opt-in. The file is
    fully rebuilt on every startup, so removing an entity's `icons` option
    also removes it here.
    """
    icons_by_key: dict[str, dict] = {}
    for entry in config.get(CLIMATE_DOMAIN, []):
        if not isinstance(entry, dict) or entry.get("platform") != DOMAIN:
            continue

        translation_key = derive_translation_key(entry)
        icons = entry.get(CONF_ICONS)
        if not icons or not translation_key:
            continue

        icons_by_key[translation_key] = _merge_icons(
            icons_by_key.get(translation_key, {}), icons
        )

    content = {"entity": {CLIMATE_DOMAIN: icons_by_key}}

    try:
        ICONS_PATH.write_text(json.dumps(content, indent=2, sort_keys=True) + "\n")
    except OSError:
        _LOGGER.exception("Failed to write generated %s", ICONS_PATH)


def _merge_icons(existing: dict, icons: dict) -> dict:
    """Merge one entity's `icons` option into the icons.json entry for its key."""
    merged = dict(existing)
    if "default" in icons:
        merged["default"] = icons["default"]
    if "state" in icons:
        merged["state"] = icons["state"]
    if "state_attributes" in icons:
        state_attributes = dict(merged.get("state_attributes", {}))
        state_attributes.update(icons["state_attributes"])
        merged["state_attributes"] = state_attributes
    return merged

