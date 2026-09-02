"""The climate template component."""

import json
import logging
from pathlib import Path

from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN

from .climate import CONF_ICONS, CONF_TRANSLATIONS, DOMAIN, derive_translation_key

_LOGGER = logging.getLogger(__name__)

COMPONENT_PATH = Path(__file__).parent
ICONS_PATH = COMPONENT_PATH / "icons.json"
TRANSLATIONS_PATH = COMPONENT_PATH / "translations"


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
    await hass.async_add_executor_job(_generate_icons_and_translations, config)
    return True


def _generate_icons_and_translations(config):
    """Regenerate icons.json and translations/<lang>.json from entity YAML options.

    Config validation has already turned every "platform: climate_template"
    block under "climate:" into a dict shaped by PLATFORM_SCHEMA (this runs
    before any component's async_setup), so we can read it straight from the
    raw config instead of waiting on per-entity async_setup_platform calls.
    Entities without a derivable identifier (see `derive_translation_key`) are
    skipped, keeping the feature fully opt-in. icons.json is always fully
    rebuilt, so removing an entity's `icons` option also removes it there.
    translations/<lang>.json files are only (re)written for languages
    currently referenced in config; a language removed from every entity's
    `translations` option is left on disk until manually deleted -- unlike
    icons.json, has_translations is only detected once at Home Assistant
    startup, so the `translations` directory (with a checked-in `en.json`
    placeholder) must already exist for translations to load at all.
    """
    icons_by_key: dict[str, dict] = {}
    translations_by_lang: dict[str, dict[str, dict]] = {}

    for entry in config.get(CLIMATE_DOMAIN, []):
        if not isinstance(entry, dict) or entry.get("platform") != DOMAIN:
            continue

        translation_key = derive_translation_key(entry)
        if not translation_key:
            continue

        if icons := entry.get(CONF_ICONS):
            icons_by_key[translation_key] = _merge_state_block(
                icons_by_key.get(translation_key, {}), icons
            )

        for lang, lang_block in (entry.get(CONF_TRANSLATIONS) or {}).items():
            by_key = translations_by_lang.setdefault(lang, {})
            by_key[translation_key] = _merge_state_block(
                by_key.get(translation_key, {}), lang_block
            )

    _write_json(ICONS_PATH, {"entity": {CLIMATE_DOMAIN: icons_by_key}})

    if translations_by_lang:
        TRANSLATIONS_PATH.mkdir(exist_ok=True)
    for lang, by_key in translations_by_lang.items():
        _write_json(
            TRANSLATIONS_PATH / f"{lang}.json", {"entity": {CLIMATE_DOMAIN: by_key}}
        )


def _merge_state_block(existing: dict, block: dict) -> dict:
    """Merge one entity's `icons`/`translations` option into its accumulated entry.

    Shared by icons.json ("default"/"state"/"state_attributes") and
    translations/<lang>.json ("name"/"state"/"state_attributes"), which both
    key entries by entity.climate.<translation_key>.
    """
    merged = dict(existing)
    for key in ("name", "default", "state"):
        if key in block:
            merged[key] = block[key]
    if "state_attributes" in block:
        state_attributes = dict(merged.get("state_attributes", {}))
        state_attributes.update(block["state_attributes"])
        merged["state_attributes"] = state_attributes
    return merged


def _write_json(path: Path, content: dict) -> None:
    try:
        path.write_text(
            json.dumps(content, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except OSError:
        _LOGGER.exception("Failed to write generated %s", path)
