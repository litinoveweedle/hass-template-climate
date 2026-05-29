# Changelog

All notable changes across all fork generations are documented here.

---

## [mikopp/hass-template-climate](https://github.com/mikopp/hass-template-climate) — this fork

### 2026-05-29 — Humidity control without dry HVAC mode

- **Author:** [@mikopp](https://github.com/mikopp)
- **Added:** Enables `set_humidity` and `target_humidity_template` without requiring `dry` in `hvac_modes`.

### 2026-05-12 — [PR #2](https://github.com/mikopp/hass-template-climate/pull/2) — Fix CONF_AVAILABILITY import error

- **Author:** [@mikopp](https://github.com/mikopp)
- **Fixed:** `CONF_AVAILABILITY` was removed from `homeassistant.const` in HA 2025.x; defined locally instead.

### 2026-05-12 — [PR #1](https://github.com/mikopp/hass-template-climate/pull/1) — Integrate attributes support, fix schema and availability

- **Author:** [@mikopp](https://github.com/mikopp)
- **Added:** `temp_step_template` — template-based dynamic temperature step size. Overrides the static `temp_step` when set. Sourced from [@bernadoDavinci](https://github.com/bernadoDavinci/hass-template-climate/commit/02e4c4588bd673ea3c1e8d1476df58bfdefe8a55).
- **Fixed:** `attributes` and `variables` in config were silently ignored. Switched to `make_template_entity_common_modern_attributes_schema` and merged `_attr_extra_state_attributes` into `extra_state_attributes`. Sourced from upstream [jcwillox PR #125](https://github.com/jcwillox/hass-template-climate/pull/125) and [PR #134](https://github.com/jcwillox/hass-template-climate/pull/134).
- **Fixed:** `availability_template` was accepted by the schema but never read by HA's `TemplateEntity`. Maps `availability_template` → `availability` in `__init__` before `super().__init__()`.
- **Deprecated:** `modes` → `hvac_modes`, `availability_template` → `availability`, `icon_template` → `icon`, `entity_picture_template` → `picture` (deprecated aliases kept, log warning at startup).

---

## Breaking Changes from [jcwillox/hass-template-climate](https://github.com/jcwillox/hass-template-climate)

- `modes` renamed to `hvac_modes` (deprecated alias kept — see above).
- `hvac_modes` defaults to `["off", "heat"]` instead of all six modes.
- `preset_modes`, `fan_modes`, `swing_modes` are empty by default.

---

## [litinoveweedle/hass-template-climate](https://github.com/litinoveweedle/hass-template-climate) — upstream fork history

### 2025-08-12 — [PR #29](https://github.com/litinoveweedle/hass-template-climate/pull/29) — Compatibility overhaul for HA 2025.8.0

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed compatibility with Home Assistant 2025.8.0 API changes.

### 2024-07-26 — [PR #25](https://github.com/litinoveweedle/hass-template-climate/pull/25) — Fix heat_cool temperature ranges in UI

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed `heat_cool` temperature range handling in the UI.

### 2024-06-22 — [PR #23](https://github.com/litinoveweedle/hass-template-climate/pull/23) — Conditional temperature and humidity targets

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Temperature and humidity targets are now enabled conditionally based on configuration.

### 2024-05-14 — [PR #21](https://github.com/litinoveweedle/hass-template-climate/pull/21) — Fix HomeAssistantType deprecation warning

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Replaced deprecated `HomeAssistantType` with current type.

### 2024-05-14 — [PR #20](https://github.com/litinoveweedle/hass-template-climate/pull/20) — Preset modes: improved docs

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Explicitly listed all allowed HVAC modes in documentation.

### 2024-05-14 — [PR #19](https://github.com/litinoveweedle/hass-template-climate/pull/19) — Preset modes as climate profiles

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Implemented presets as climate profiles. Loosened configuration checks for less common use cases.

### 2024-04-22 — [PR #16](https://github.com/litinoveweedle/hass-template-climate/pull/16) — Preset modes: named variables and debug logging

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed named variables for climate entity HA functions. Changed `set_temperature` to mimic HA behavior (always set any attribute). Added more debug logging.

### 2024-04-22 — [PR #15](https://github.com/litinoveweedle/hass-template-climate/pull/15) — Preset modes: fix type check

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed invalid type check for previous attributes restore.

### 2024-04-21 — [PR #14](https://github.com/litinoveweedle/hass-template-climate/pull/14) — Preset modes: fix re-trigger logic

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed re-trigger action logic for attributes without templates.

### 2024-04-21 — [PR #13](https://github.com/litinoveweedle/hass-template-climate/pull/13) — Preset modes refactor

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Refactored callbacks. Use configuration defaults for modes. Fixed typos in logging.

### 2024-04-20 — [PR #11](https://github.com/litinoveweedle/hass-template-climate/pull/11) — Fix "Already running" warning

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Improved logging messages. Fixed "Already running" for some cases: do not execute script if attribute value has not changed. Full code refactoring and input validation.

### 2024-04-06 — [PR #7](https://github.com/litinoveweedle/hass-template-climate/pull/7) — Fix missing context when running script

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed missing context when running scripts. Sourced from [home-assistant/core#113523](https://github.com/home-assistant/core/pull/113523).

### 2024-04-05 — [PR #5](https://github.com/litinoveweedle/hass-template-climate/pull/5) — Fix fan and swing mode

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed current fan and swing mode initialization.

### 2024-04-05 — [PR #4](https://github.com/litinoveweedle/hass-template-climate/pull/4) — HA Climate Entity Features compatibility

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Added support for Climate Entity Features flags including `turn_on` and `turn_off` services.

### 2023-12-29 — [PR #3](https://github.com/litinoveweedle/hass-template-climate/pull/3) — Add target_humidity and set_humidity

- **Author:** [@isottipietro](https://github.com/isottipietro)
- Added `target_humidity` template support and `set_humidity` service call.

### 2023-12-29 — [PR #2](https://github.com/litinoveweedle/hass-template-climate/pull/2) — Run mode support

- **Author:** [@devildant](https://github.com/devildant)
- Added run mode functionality.

### 2023-12-29 — [PR #1](https://github.com/litinoveweedle/hass-template-climate/pull/1) — Preset mode

- **Author:** [@scuba75](https://github.com/scuba75)
- Added preset mode option.

---

## [jcwillox/hass-template-climate](https://github.com/jcwillox/hass-template-climate) — original repo history

### 2023-01-28 — [PR #33](https://github.com/jcwillox/hass-template-climate/pull/33) — Allow hvac_action to be None

- **Author:** [@laszlojakab](https://github.com/laszlojakab)

### 2022-11-18 — [PR #27](https://github.com/jcwillox/hass-template-climate/pull/27) — Add support for unique_id

- **Author:** [@laszlojakab](https://github.com/laszlojakab)

### 2022-11-12 — [PR #24](https://github.com/jcwillox/hass-template-climate/pull/24) — Add support for hvac_action template

- **Author:** [@laszlojakab](https://github.com/laszlojakab)

### 2022-07-05 — [PR #9](https://github.com/jcwillox/hass-template-climate/pull/9) — Add example climate.set_hvac_mode action

- **Author:** [@JOHLC](https://github.com/JOHLC)

### 2022-06-11 — [PR #7](https://github.com/jcwillox/hass-template-climate/pull/7) — Pass variables to set_* scripts

- **Author:** Artem Sorokin

### 2022-06-11 — [PR #6](https://github.com/jcwillox/hass-template-climate/pull/6) — Add templates for target_temperature, hvac_mode, fan_mode

- **Author:** Artem Sorokin
