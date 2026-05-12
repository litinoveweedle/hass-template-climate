# Changelog

All notable changes to this fork are documented here.

---

## [Unreleased]

### Added

- **`temp_step_template`** — Template-based dynamic temperature step size. Overrides the static `temp_step` when set. Sourced from [@bernadoDavinci](https://github.com/bernadoDavinci/hass-template-climate/commit/02e4c4588bd673ea3c1e8d1476df58bfdefe8a55).

### Fixed

- **`attributes` and `variables` support** — Custom state attributes and script variables defined in config were silently ignored. Fixed by switching to `make_template_entity_common_modern_attributes_schema` (adds `attributes`, `variables`, `availability` to the valid schema) and merging `_attr_extra_state_attributes` into the `extra_state_attributes` property. Sourced from upstream PRs [#125](https://github.com/jcwillox/hass-template-climate/pull/125) and [#134](https://github.com/jcwillox/hass-template-climate/pull/134) by [@jcwillox](https://github.com/jcwillox).

- **`availability_template` broken** — The `availability_template` key was accepted by the schema but never read by HA's `TemplateEntity` (which only reads `availability`). Fixed by mapping `availability_template` → `availability` in `__init__` before `super().__init__()` is called.

### Deprecated

The following config keys still work but log a deprecation warning at startup. Please migrate to the replacement key.

| Deprecated key            | Replacement    |
| ------------------------- | -------------- |
| `modes`                   | `hvac_modes`   |
| `availability_template`   | `availability` |
| `icon_template`           | `icon`         |
| `entity_picture_template` | `picture`      |

---

## Breaking Changes from [jcwillox/hass-template-climate](https://github.com/jcwillox/hass-template-climate)

- `modes` renamed to `hvac_modes` (deprecated alias kept — see above).
- `hvac_modes` defaults to `["off", "heat"]` instead of all six modes.
- `preset_modes`, `fan_modes`, `swing_modes` are empty by default.
