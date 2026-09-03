# Changelog

All notable changes across all fork generations are hopefully documented here.

---

### 2026-09-03 — Document translations startup race limitation

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Documented a known limitation where Home Assistant's own eager translation preload (started before this integration regenerates `translations/<lang>.json` at startup) can race the file write, most visibly right after a HACS update resets the file to its placeholder. Icons are unaffected; a second restart self-corrects.


### 2026-09-03 — `0.8.1` - HA 2026.9.0 compatibility changes
- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- fixes for breaking changes in the HA 2026.9.0


### 2026-09-02 — `0.8.0` - [PR #43](https://github.com/litinoveweedle/hass-template-climate/pull/43) — Custom icons and translations

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Added configuration-driven generation of Home Assistant icon translations for `hvac_mode`, `fan_mode`, `preset_mode`, and `swing_mode`.
- Added configuration-driven generation of per-language entity state and state-attribute translations.
- **Contributed by:** [@BirbByte](https://github.com/BirbByte) for the custom icon implementation.


### 2026-09-02 — Warn about deprecated configuration options

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Added startup warnings for legacy configuration fields and the deprecated `entity_id` option, including the affected entity name and migration target.


### 2026-09-02 — [PR #42](https://github.com/litinoveweedle/hass-template-climate/pull/42) — Ruff fixes and HEAT_COOL handling

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Added template support for `temp_step`, `precision`, `min_temp`, `max_temp`, `min_humidity`, and `max_humidity`.
- Fixed `HEAT_COOL` temperature handling.
- Applied Ruff and code-standardization fixes.
- **Based in part on:** [@mikopp's unmerged PR #1](https://github.com/mikopp/hass-template-climate/pull/1) and [PR #2](https://github.com/mikopp/hass-template-climate/pull/2), which provided earlier work on template attributes, availability handling, and Home Assistant compatibility.


### 2026-07-02 — `0.7.7` — Fix template updates

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed an issue where templates did not update correctly after setup or reload.


### 2026-06-04 — `v1.4.0` — [PR #141](https://github.com/litinoveweedle/hass-template-climate/pull/141) — Home Assistant 2026.6 compatibility

- **Author:** [@Petro31](https://github.com/Petro31)
- Updated the integration for Home Assistant 2026.6 compatibility.


### 2026-06-02 — `0.7.6` — Preset class

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Refactored preset handling into a dedicated class.


### 2026-06-01 — State-update fixes

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed state updates, humidity updates, and a `preset_mode` race condition.


### 2025-08-12 — `0.7.4` — [PR #29](https://github.com/litinoveweedle/hass-template-climate/pull/29) — Compatibility overhaul for HA 2025.8.0

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed compatibility with Home Assistant 2025.8.0 API changes.


### 2024-07-26 — `0.7.3` — [PR #25](https://github.com/litinoveweedle/hass-template-climate/pull/25) — Fix heat_cool temperature ranges in UI

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed `heat_cool` temperature range handling in the UI.


### 2024-06-22 — `0.7.2` — [PR #23](https://github.com/litinoveweedle/hass-template-climate/pull/23) — Conditional temperature and humidity targets

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Temperature and humidity targets are now enabled conditionally based on configuration.


### 2024-05-14 — `0.7.1` — [PR #21](https://github.com/litinoveweedle/hass-template-climate/pull/21) — Fix HomeAssistantType deprecation warning

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


### 2024-04-20 — `0.7.0` — [PR #11](https://github.com/litinoveweedle/hass-template-climate/pull/11) — Fix "Already running" warning

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Improved logging messages. Fixed "Already running" for some cases: do not execute script if attribute value has not changed. Full code refactoring and input validation.


### 2024-04-06 — `0.6.4` — [PR #7](https://github.com/litinoveweedle/hass-template-climate/pull/7) — Fix missing context when running script

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed missing context when running scripts. Sourced from [home-assistant/core#113523](https://github.com/home-assistant/core/pull/113523).


### 2024-04-05 — [PR #5](https://github.com/litinoveweedle/hass-template-climate/pull/5) — Fix fan and swing mode

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Fixed current fan and swing mode initialization.


### 2024-04-05 — [PR #4](https://github.com/litinoveweedle/hass-template-climate/pull/4) — HA Climate Entity Features compatibility

- **Author:** [@litinoveweedle](https://github.com/litinoveweedle)
- Added support for Climate Entity Features flags including `turn_on` and `turn_off` services.


### 2023-12-29 — `0.6.2` — [PR #3](https://github.com/litinoveweedle/hass-template-climate/pull/3) — Add target_humidity and set_humidity

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

### 2023-01-28 — `0.6.1`, `v0.6.1` — [PR #33](https://github.com/jcwillox/hass-template-climate/pull/33) — Allow hvac_action to be None

- **Author:** [@laszlojakab](https://github.com/laszlojakab)


### 2022-11-18 — `0.6.0` — [PR #27](https://github.com/jcwillox/hass-template-climate/pull/27) — Add support for unique_id

- **Author:** [@laszlojakab](https://github.com/laszlojakab)


### 2022-11-12 — `0.5.0` — [PR #24](https://github.com/jcwillox/hass-template-climate/pull/24) — Add support for hvac_action template

- **Author:** [@laszlojakab](https://github.com/laszlojakab)


### 2022-07-05 — [PR #9](https://github.com/jcwillox/hass-template-climate/pull/9) — Add example climate.set_hvac_mode action

- **Author:** [@JOHLC](https://github.com/JOHLC)


### 2022-06-11 — `0.3.0` — [PR #7](https://github.com/jcwillox/hass-template-climate/pull/7) — Pass variables to set_* scripts

- **Author:** Artem Sorokin


### 2022-06-11 — [PR #6](https://github.com/jcwillox/hass-template-climate/pull/6) — Add templates for target_temperature, hvac_mode, fan_mode

- **Author:** Artem Sorokin