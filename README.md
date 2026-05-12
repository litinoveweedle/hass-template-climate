# ❄️ Template Climate

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/litinoveweedle/hass-template-climate?style=for-the-badge)](https://github.com/litinoveweedle/hass-template-climate/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/litinoveweedle/hass-template-climate?style=for-the-badge)](https://github.com/litinoveweedle/hass-template-climate/releases)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

The `climate_template` platform creates climate devices that combine integrations and provides the ability to run scripts or invoke services for each of the `set_*` commands of a climate entity.

## Disclaimer

This is a fork of the original [jcwillox/hass-template-climate](https://github.com/jcwillox/hass-template-climate) repository, which appears to be unmaintained with several useful pull requests pending. This fork merges those PRs and adds additional functionality. All credit for the original work belongs to the original authors. Note that there are some **breaking changes** from the original version — see [below](#breaking-changes-from-jcwillox-versions).

## Breaking Changes from jcwillox Versions

- Config key `modes` renamed to `hvac_modes` (**`modes` still works but is deprecated — a warning will be logged**)
- `hvac_modes` defaults to `["off", "heat"]` instead of all modes
- `preset_modes`, `fan_modes` and `swing_modes` are empty by default — only configure what you actually use

## Preset Modes as Preset Profiles

Preset modes can function as full profiles: each preset can store hvac mode, fan mode, swing mode, target temperatures, and humidity. Values are editable via the HA UI and preserved across restarts. Three config options control this: `presets_features`, `presets_template`, and `set_presets`.

### presets_features

Bit-flag sum defining which features are managed by presets:

| Value | Feature |
|-------|---------|
| 1 | Preset attributes are changeable via HA |
| 2 | Preset attributes are preserved over HA restarts |
| 4 | HVAC mode is a preset attribute |
| 8 | Fan mode is a preset attribute |
| 16 | Swing mode is a preset attribute |
| 32 | Target temperature is a preset attribute |
| 64 | High/low temperature are preset attributes |
| 128 | Target humidity is a preset attribute |

Set `presets_features` to the sum of desired values. `0` disables presets.

### presets_template

Returns a dictionary of all presets and their attributes (used to sync state from the managed device back to HA):

```
'some_preset_name': {
  'hvac_mode': 'heat',
  'fan_mode': 'on',
  'swing_mode': 'fast',
  'target_temperature': 22,
  'target_temperature_low': 19,
  'target_temperature_high': 23
},
'other_preset_name': {
  'hvac_mode': 'off',
  ...
}
```

### set_presets

Action called when a preset attribute changes in HA. Receives two variables:
- `presets` — complete dict of all presets with all managed attribute values
- `changed` — only the preset and attribute that triggered the run, e.g. `{'some_preset_name': {'target_temperature': 24}}`

## Configuration

All configuration variables are optional. The climate device will work in optimistic mode (assumed state) if a template is not defined. If neither a `template` nor its corresponding `action` is defined for a feature, that feature will not be registered (e.g. both `swing_mode_template` and `set_swing_mode` must be absent for the entity to have no swing mode).

| Name                             | Type                                                                      | Description                                                                                                                                                                                                                                                                                     | Default Value                           |
| -------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| name                             | `string` or [`template`](https://www.home-assistant.io/docs/configuration/templating) | The name of the climate device.                                                                                                                                                                                                                                                 | "Template Climate"                      |
| unique_id                        | `string`                                                                  | The [unique id](https://developers.home-assistant.io/docs/entity_registry_index/#unique-id) of the climate entity.                                                                                                                                                                              | None                                    |
| icon                             | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template for the icon of the entity.                                                                                                                                                                                                                                                  |                                         |
| picture                          | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template for the entity picture.                                                                                                                                                                                                                                                      |                                         |
| attributes                       | `dict`                                                                    | Dictionary of `name: template` pairs defining extra state attributes to expose on the entity. Each value is rendered as a template.                                                                                                                                                             |                                         |
| variables                        | `dict`                                                                    | Additional variables available in all action scripts (e.g. `set_hvac_mode`).                                                                                                                                                                                                                   |                                         |
| availability                     | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Template returning `true` when the entity is available. If not set, the entity is always available.                                                                                                                                                                                             | true                                    |
| mode_action                      | `string`                                                                  | Script execution mode: `parallel`, `queued`, `restart`, or `single`. See [`script`](https://www.home-assistant.io/integrations/script/#script-modes) docs.                                                                                                                                      | single                                  |
| max_action                       | `positive_int`                                                            | Max concurrent action runs. Used with `parallel` and `queued` mode_action. See [`script`](https://www.home-assistant.io/integrations/script/#max) docs.                                                                                                                                         | 1                                       |
| presets_features                 | `positive_int`                                                            | Bit-flag sum of preset features. See [Preset Modes](#preset-modes-as-preset-profiles). `0` disables presets.                                                                                                                                                                                    | 0                                       |
|                                  |                                                                           |                                                                                                                                                                                                                                                                                                 |                                         |
| current_temperature_template     | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the current temperature.                                                                                                                                                                                                                                              |                                         |
| current_humidity_template        | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the current humidity.                                                                                                                                                                                                                                                 |                                         |
| target_temperature_template      | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the target temperature.                                                                                                                                                                                                                                               |                                         |
| target_temperature_low_template  | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the target temperature low (used with `heat_cool` hvac_mode).                                                                                                                                                                                                         |                                         |
| target_temperature_high_template | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the target temperature high (used with `heat_cool` hvac_mode).                                                                                                                                                                                                        |                                         |
| target_humidity_template         | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the target humidity.                                                                                                                                                                                                                                                  |                                         |
| min_humidity_template            | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the minimum target humidity.                                                                                                                                                                                                                                          |                                         |
| max_humidity_template            | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the maximum target humidity.                                                                                                                                                                                                                                          |                                         |
| hvac_mode_template               | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the current hvac mode.                                                                                                                                                                                                                                                |                                         |
| fan_mode_template                | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the current fan mode.                                                                                                                                                                                                                                                 |                                         |
| preset_mode_template             | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the current preset mode.                                                                                                                                                                                                                                              |                                         |
| swing_mode_template              | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the current swing mode.                                                                                                                                                                                                                                               |                                         |
| hvac_action_template             | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the [`hvac action`](https://developers.home-assistant.io/docs/core/entity/climate/#hvac-action) (e.g. `heating`, `cooling`, `idle`, `fan`).                                                                                                                           |                                         |
| presets_template                 | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Returns all preset values as a dictionary. See [presets_template](#presets_template) for the required structure.                                                                                                                                                                                 |                                         |
|                                  |                                                                           |                                                                                                                                                                                                                                                                                                 |                                         |
| set_temperature                  | [`action`](https://www.home-assistant.io/docs/scripts)                    | Action when set temperature is called. Variables: `temperature`, `target_temp_high`, `target_temp_low`, `hvac_mode`.                                                                                                                                                                             |                                         |
| set_humidity                     | [`action`](https://www.home-assistant.io/docs/scripts)                    | Action when set humidity is called. Variable: `humidity`.                                                                                                                                                                                                                                       |                                         |
| set_hvac_mode                    | [`action`](https://www.home-assistant.io/docs/scripts)                    | Action when set hvac mode is called. Variable: `hvac_mode`.                                                                                                                                                                                                                                     |                                         |
| set_fan_mode                     | [`action`](https://www.home-assistant.io/docs/scripts)                    | Action when set fan mode is called. Variable: `fan_mode`.                                                                                                                                                                                                                                       |                                         |
| set_preset_mode                  | [`action`](https://www.home-assistant.io/docs/scripts)                    | Action when set preset mode is called. Variable: `preset_mode`.                                                                                                                                                                                                                                 |                                         |
| set_swing_mode                   | [`action`](https://www.home-assistant.io/docs/scripts)                    | Action when set swing mode is called. Variable: `swing_mode`.                                                                                                                                                                                                                                   |                                         |
| set_presets                      | [`action`](https://www.home-assistant.io/docs/scripts)                    | Action when a preset attribute changes. Variables: `presets` (all presets) and `changed` (only updated value). See [set_presets](#set_presets).                                                                                                                                                  |                                         |
|                                  |                                                                           |                                                                                                                                                                                                                                                                                                 |                                         |
| hvac_modes                       | `list`                                                                    | Supported hvac modes. Must be a subset of: `off`, `heat`, `cool`, `heat_cool`, `auto`, `dry`, `fan_only`. See [hvac_modes](https://developers.home-assistant.io/docs/core/entity/climate/#hvac-modes).                                                                                           | `["off", "heat"]`                       |
| preset_modes                     | `list`                                                                    | Supported preset modes. Custom values allowed. See [preset_modes](https://developers.home-assistant.io/docs/core/entity/climate/#presets).                                                                                                                                                       |                                         |
| fan_modes                        | `list`                                                                    | Supported fan modes. Custom values allowed. See [fan_modes](https://developers.home-assistant.io/docs/core/entity/climate/#fan-modes).                                                                                                                                                           |                                         |
| swing_modes                      | `list`                                                                    | Supported swing modes. Custom values allowed.                                                                                                                                                                                                                                                   |                                         |
|                                  |                                                                           |                                                                                                                                                                                                                                                                                                 |                                         |
| min_temp                         | `float`                                                                   | Minimum temperature set point available.                                                                                                                                                                                                                                                        | 7                                       |
| max_temp                         | `float`                                                                   | Maximum temperature set point available.                                                                                                                                                                                                                                                        | 35                                      |
| min_humidity                     | `float`                                                                   | Minimum humidity set point available.                                                                                                                                                                                                                                                           | 30                                      |
| max_humidity                     | `float`                                                                   | Maximum humidity set point available.                                                                                                                                                                                                                                                           | 99                                      |
| precision                        | `float`                                                                   | The desired precision for this device.                                                                                                                                                                                                                                                          | 0.1 for Celsius, 1.0 for Fahrenheit     |
| temp_step                        | `float`                                                                   | Step size for temperature set point.                                                                                                                                                                                                                                                            | 1                                       |

## Deprecated Keys

The following config keys still work but will log a deprecation warning. Please migrate to the replacement.

| Deprecated Key            | Replacement    | Notes                                                        |
| ------------------------- | -------------- | ------------------------------------------------------------ |
| `modes`                   | `hvac_modes`   | Renamed in this fork. Automatically mapped on load.          |
| `availability_template`   | `availability` | HA template entity standard. Automatically mapped on load.   |
| `icon_template`           | `icon`         | HA template entity standard.                                 |
| `entity_picture_template` | `picture`      | HA template entity standard.                                 |

## Example Configuration

```yaml
climate:
  - platform: climate_template
    name: Bedroom Aircon
    hvac_modes:
      - "auto"
      - "dry"
      - "off"
      - "cool"
      - "fan_only"
    min_temp: 16
    max_temp: 30

    current_temperature_template: "{{ states('sensor.bedroom_temperature') }}"
    current_humidity_template: "{{ states('sensor.bedroom_humidity') }}"
    swing_mode_template: "{{ states('input_boolean.bedroom_swing_mode') }}"
    availability: "{{ is_state('binary_sensor.bedroom_node_status', 'on') }}"

    set_hvac_mode:
      - condition: state
        entity_id: input_boolean.enable_aircon_controller
        state: "on"
      - service: esphome.bedroom_node_aircon_state
        data:
          temperature: "{{ state_attr('climate.bedroom_aircon', 'temperature') | int }}"
          operation_mode: "{{ states('climate.bedroom_aircon') }}"
          fan_mode: "{{ state_attr('climate.bedroom_aircon', 'fan_mode') }}"
          swing_mode: "{{ is_state_attr('climate.bedroom_aircon', 'swing_mode', 'on') }}"
          light: "{{ is_state('light.bedroom_aircon_light', 'on') }}"
```

### Example: extra state attributes

```yaml
climate:
  - platform: climate_template
    name: Airflow Controller
    hvac_modes:
      - "off"
      - "cool"
    attributes:
      outdoor_temp: "{{ states('sensor.outdoor_temp') | float(none) }}"
      indoor_dew: "{{ states('sensor.indoor_dew') | float(none) }}"
      free_cooling_available: "{{ is_state('binary_sensor.free_cooling_available', 'on') }}"
```

### Example: variables in actions

```yaml
climate:
  - platform: climate_template
    name: My Climate
    variables:
      device_id: "my_esphome_device"
    set_hvac_mode:
      - service: esphome.{{ device_id }}_set_mode
        data:
          mode: "{{ hvac_mode }}"
```

### Example: control an existing Home Assistant climate device

```yaml
climate:
  - platform: climate_template
    # ...
    set_hvac_mode:
      - service: climate.set_hvac_mode
        data:
          entity_id: climate.bedroom_ac_nottemplate
          hvac_mode: "{{ states('climate.bedroom_ac_template') }}"
```

### Example: preset profiles for a boiler with multiple heating modes

```yaml
climate:
  - platform: climate_template
    name: "Heating Circuit 1"
    unique_id: "climate_template_heating_hc1"
    mode_action: "queued"
    max_action: 3
    hvac_modes:
      - "heat"
    preset_modes:
      - "automatic"
      - "comfort"
      - "reduced"
      - "protection"
    # 1 (editable) + 2 (saved) + 32 (target temperature) = 35
    presets_features: 35
    min_temp: 10
    max_temp: 30
    temp_step: 0.5
    current_temperature_template: "{{ states('sensor.boiler_hc1_room_temperature_actual_value') }}"
    hvac_mode_template: "heat"
    preset_mode_template: "{{ states('select.boiler_hc1_operating_mode') | lower }}"
    presets_template: >
      {{ {
        'automatic': { 'target_temperature': states('number.boiler_hc1_room_temperature_comfort_setpoint') },
        'comfort':   { 'target_temperature': states('number.boiler_hc1_room_temperature_comfort_setpoint') },
        'reduced':   { 'target_temperature': states('number.boiler_hc1_room_temperature_reduced_setpoint') },
        'protection':{ 'target_temperature': states('number.boiler_hc1_room_temperature_protection_setpoint') }
      } }}
    hvac_action_template: "{% if 'Heating' in states('sensor.boiler_hc1_status') %}heating{% else %}idle{% endif %}"
    set_presets:
      - if:
          - condition: template
            value_template: "{{ ('automatic' in changed and 'target_temperature' in changed.automatic) or ('comfort' in changed and 'target_temperature' in changed.comfort) }}"
        then:
          - service: number.set_value
            target:
              entity_id: "number.boiler_hc1_room_temperature_comfort_setpoint"
            data:
              value: "{{ (changed.automatic | default(changed.comfort)).target_temperature }}"
      - if:
          - condition: template
            value_template: "{{ 'reduced' in changed and 'target_temperature' in changed.reduced }}"
        then:
          - service: number.set_value
            target:
              entity_id: "number.boiler_hc1_room_temperature_reduced_setpoint"
            data:
              value: "{{ changed.reduced.target_temperature }}"
      - if:
          - condition: template
            value_template: "{{ 'protection' in changed and 'target_temperature' in changed.protection }}"
        then:
          - service: number.set_value
            target:
              entity_id: "number.boiler_hc1_room_temperature_protection_setpoint"
            data:
              value: "{{ changed.protection.target_temperature }}"
    set_preset_mode:
      - service: select.select_option
        target:
          entity_id: select.boiler_hc1_operating_mode
        data:
          option: "{{ preset_mode | title }}"
```

## Use Cases

- Merge multiple components into one climate device (just like any template platform).
- Control optimistic climate devices such as IR aircons via service calls.
- Wrap an existing HA climate entity to add custom attributes, logic, or preset profiles.
