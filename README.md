# ❄️ Template Climate

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/litinoveweedle/hass-template-climate?style=for-the-badge)](https://github.com/litinoveweedle/hass-template-climate/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/litinoveweedle/hass-template-climate?style=for-the-badge)](https://github.com/litinoveweedle/hass-template-climate/releases)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

The `climate_template` platform creates climate devices that combine integrations and provides the ability to run scripts or invoke services for each of the `set_*` commands of a climate entity.

## Disclaimer

This is a fork of the original repository jcwillox/hass-template-climate, which appears to be unmaintained at the time and had several pull requests pending. As those were very useful for my usage, I decided to fork and merge the work of the corresponding authors to allow for simple usage of the integration through HACS. Therefore, all the corresponding rights belong to the original authors. I also started fixing additional user issues and adding functionality while trying to maintain compatibility, but please note that there are some **breaking changes** from the original version.

## Breaking changes from jcwillox versions

- Config parameter `modes` renamed to `hvac_modes`
- `hvac_modes` list is set only to `["off", "heat"]` by default.
- `preset_modes`, `fan_modes` and `swing_modes` are now not set by default and shall be configured **only** if being used and set to the used miminum list of modes.

## Preset modes as profiles

For a long time, I wanted climate preset modes to function as profiles. So you can have a profile that defines any climate attributes such as HVAC mode, fan mode, swing mode, target temperatures, and humidity, and by a single click activate that profile. Users should be able to modify any given preset attribute value using both the HA GUI and service calls. Also, set preset attribute values should be preserved across HA restarts. Now all of this is possible! To control this feature, three new configuration options — `presets_features`, `presets_template`, and `set_presets` — were introduced.

### presets_features
`presets_features` is a bit flag used to identify which parameters (HVAC mode, fan mode, swing mode, target temperatures, and humidity) you would like to manage with presets:

1 - preset attributes are changeable via HA\
2 - preset attributes are preserved across HA restarts\
4 - HVAC mode is a preset attribute\
8 - fan mode is a preset attribute\
16 - swing mode is a preset attribute\
32 - target temperature is a preset attribute\
64 - high/low temperature are preset attributes\
128 - target humidity is a preset attribute

The `presets_features` value should be the sum of all active feature values as above. If set to 0, presets are disabled.

### presets_template
`presets_template` — if it is possible to set or change preset attributes directly on the managed device and you need to sync changes back to HA, you need to provide `presets_template`, which returns a dictionary object containing all presets, each containing every preset attribute. Example of the return object with all preset attributes managed:

```
'some_preset_name': {
  'hvac_mode': 'heat',
  'fan_mode": 'on',
  'swing_mode": 'fast',
  'target_temperature': 22,
  'target_temperature_low': 19,
  'target_temperature_high': 23
},
'other_preset_name': {
  'hvac_mode': 'off',
  ....
}, ...
```

### set_presets
`set_presets` - it is template to set / synchronize managed device presets atributes to the values managed in HomeAssistant. Therefore if you change preset attribute value in HA it will be propagated to the managed device. This template is called with two variables, `presets` variable contains complete list of all presets, each will all managed presets attributes i.e.:

```
'some_preset_name': {
  'hvac_mode': 'heat',
  'fan_mode": 'on',
  'swing_mode": 'fast',
  'target_temperature': 22,
  'target_temperature_low': 19,
  'target_temperature_high': 23
},
'other_preset_name': {
  'hvac_mode': 'off',
  ....
}, ...
```

The other valiable `changed` only contains the preset mode and attribute which triggered the run:

```
{'some_preset_name': { 'target_temperature': 24 } }
```

Please check example presets configuration bellow to see how to both construct required dictionary objects and how to prase those in template.

## Configuration

All configuration variables are optional. If you do not define a `template` or its corresponding `action`, the climate device will not register the given attribute/function in HA. For example, either `swing_mode_template` or `set_swing_mode` should be defined (together with allowed `swing_modes`) for the climate entity to have working swing mode functionality.

| Name                                 | Type                                                                      | Description                                                                                                                                                                                                                                                                                     | Default Value                           |
| ------------------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| name                                 | `string`                                                                  | The name of the climate device.                                                                                                                                                                                                                                                                 | "Template Climate"                      |
| unique_id                            | `string`                                                                  | The [unique id](https://developers.home-assistant.io/docs/entity_registry_index/#unique-id) of the climate entity.                                                                                                                                                                              | None                                    |
| mode_action                          | `string`                                                                  | Possible values: `parallel`, `queued`, `restart`, `single`. For explanation, see the [`script`](https://www.home-assistant.io/integrations/script/#script-modes) documentation.                                                                                                                | single                                  |
| max_action                           | `positive_int`                                                            | Limits the number of concurrent runs of actions. Used together with `parallel` and `queued` `mode_action`, set to a positive number greater than 1. For explanation, see the [`script`](https://www.home-assistant.io/integrations/script/#max) documentation.                                  | 1                                       |
| presets_features                     | `positive_int`                                                            | Define the feature flags supported by the `preset_mode` feature as bit flags. See [example](#presets_features) for options. Default value `0` means presets are disabled.                                                                                                                       | 0                                       |
| icon_template                        | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template for the icon of the sensor.                                                                                                                                                                                                                                                  |                                         |
| entity_picture_template              | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template for the entity picture of the sensor.                                                                                                                                                                                                                                        |                                         |
| availability_template                | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the `available` state of the component. If the template returns `true`, the device is `available`. If it returns any other value, the device is `unavailable`. If `availability_template` is not configured, the component will always be `available`.              | true                                    |
|                                      |                                                                           |                                                                                                                                                                                                                                                                                                 |                                         |
| current_temperature_template         | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the current temperature.                                                                                                                                                                                                                                              |                                         |
| current_humidity_template            | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the current humidity.                                                                                                                                                                                                                                                 |                                         |
| min_temp_template                    | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to dynamically set the minimum allowed target temperature.                                                                                                                                                                                                                  |                                         |
| max_temp_template                    | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to dynamically set the maximum allowed target temperature.                                                                                                                                                                                                                  |                                         |
| min_humidity_template                | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to dynamically set the minimum allowed target humidity.                                                                                                                                                                                                                     |                                         |
| max_humidity_template                | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to dynamically set the maximum allowed target humidity.                                                                                                                                                                                                                     |                                         |
| target_temperature_template          | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the target temperature of the climate device.                                                                                                                                                                                                                         |                                         |
| target_temperature_low_template      | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the low target temperature of the climate device in `heat_cool` mode.                                                                                                                                                                                                |                                         |
| target_temperature_high_template     | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the high target temperature of the climate device in `heat_cool` mode.                                                                                                                                                                                               |                                         |
| precision_template                   | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to dynamically set the desired precision for this device. Supported values are `0.1`, `0.5`, and `1`.                                                                                                                                                                      |                                         |
| temp_step_template                   | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to dynamically set the temperature step size.                                                                                                                                                                                                                               |                                         |
| presets_template                     | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get all preset values as a dictionary or JSON object. Please see [example](#presets_template) for the required data structure.                                                                                                                                             |                                         |
| target_humidity_template             | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the target humidity of the climate device.                                                                                                                                                                                                                            |                                         |
| hvac_mode_template                   | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the HVAC mode of the climate device.                                                                                                                                                                                                                                  |                                         |
| fan_mode_template                    | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the fan mode of the climate device.                                                                                                                                                                                                                                   |                                         |
| preset_mode_template                 | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the preset mode of the climate device.                                                                                                                                                                                                                                |                                         |
| swing_mode_template                  | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the swing mode of the climate device.                                                                                                                                                                                                                                 |                                         |
| hvac_action_template                 | [`template`](https://www.home-assistant.io/docs/configuration/templating) | Defines a template to get the [`hvac action`](https://developers.home-assistant.io/docs/core/entity/climate/#hvac-action) of the climate device.                                                                                                                                                |                                         |
|                                      |                                                                           |                                                                                                                                                                                                                                                                                                 |                                         |
| set_temperature                      | [`action`](https://www.home-assistant.io/docs/scripts)                    | Defines an action to run when the climate device is given the set temperature command. Can use `temperature`, `target_temp_high`, `target_temp_low`, and `hvac_mode` variables.                                                                                                                 |                                         |
| set_humidity                         | [`action`](https://www.home-assistant.io/docs/scripts)                    | Defines an action to run when the climate device is given the set humidity command. Can use the `humidity` variable.                                                                                                                                                                            |                                         |
| set_hvac_mode                        | [`action`](https://www.home-assistant.io/docs/scripts)                    | Defines an action to run when the climate device is given the set HVAC mode command. Can use the `hvac_mode` variable.                                                                                                                                                                             |                                         |
| set_fan_mode                         | [`action`](https://www.home-assistant.io/docs/scripts)                    | Defines an action to run when the climate device is given the set fan mode command. Can use the `fan_mode` variable.                                                                                                                                                                              |                                         |
| set_preset_mode                      | [`action`](https://www.home-assistant.io/docs/scripts)                    | Defines an action to run when the climate device is given the set preset mode command. Can use the `preset_mode` variable.                                                                                                                                                                        |                                         |
| set_swing_mode                       | [`action`](https://www.home-assistant.io/docs/scripts)                    | Defines an action to run when the climate device is given the set swing mode command. Can use the `swing_mode` variable.                                                                                                                                                                          |                                         |
| set_presets                          | [`action`](https://www.home-assistant.io/docs/scripts)                    | Defines an action to run when any activated preset feature value is changed. It should use the `presets` variable (all preset feature values) or the `changed` variable (only the values changed for the triggering update). See [example](#set_presets) for the variable format.            |                                         |
|                                      |                                                                           |                                                                                                                                                                                                                                                                                                 |                                         |
| hvac_modes                           | `list`                                                                    | A list of supported HVAC modes. Needs to be a subset of the default climate device [`hvac_modes`](https://developers.home-assistant.io/docs/core/entity/climate/#hvac-modes) values: `off`, `heat`, `cool`, `heat_cool`, `auto`, `dry`, `fan`                                              | ["off", "heat"]                         |
| preset_modes                         | `list`                                                                    | A list of supported preset modes. Custom preset modes are allowed. Default list of HA [`preset_modes`](https://developers.home-assistant.io/docs/core/entity/climate/#presets).                                                                                                                    |                                         |
| fan_modes                            | `list`                                                                    | A list of supported fan modes. Custom fan modes are allowed. Default list of HA [`fan_modes`](https://developers.home-assistant.io/docs/core/entity/climate/#fan-modes).                                                                                                                        |                                         |
| swing_modes                          | `list`                                                                    | A list of supported swing modes. Custom swing modes are allowed. Default list of HA [`swing_modes`](https://developers.home-assistant.io/docs/core/entity/climate/#fan-modes).                                                                                                                  |                                         |
|                                      |                                                                           |                                                                                                                                                                                                                                                                                                 |                                         |
| min_temp                             | `float`                                                                   | Minimum temperature set point available.                                                                                                                                                                                                                                                        | 7                                       |
| max_temp                             | `float`                                                                   | Maximum temperature set point available.                                                                                                                                                                                                                                                        | 35                                      |
| min_humidity                         | `float`                                                                   | Minimum humidity set point available.                                                                                                                                                                                                                                                           | 30                                      |
| max_humidity                         | `float`                                                                   | Maximum humidity set point available.                                                                                                                                                                                                                                                           | 99                                      |
| precision                            | `float`                                                                   | The desired precision for this device.                                                                                                                                                                                                                                                          | 0.1 for Celsius and 1.0 for Fahrenheit. |
| temp_step                            | `float`                                                                   | Step size for the temperature set point.                                                                                                                                                                                                                                                       | 1                                       |

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

    # get current temp.
    current_temperature_template: "{{ states('sensor.bedroom_temperature') }}"

    # get current humidity.
    current_humidity_template: "{{ states('sensor.bedroom_humidity') }}"

    # swing mode switch for UI.
    swing_mode_template: "{{ states('input_boolean.bedroom_swing_mode') }}"

    # available based on esphome nodes' availability.
    availability_template: "{{ is_state('binary_sensor.bedroom_node_status', 'on') }}"

    # example action
    set_hvac_mode:
      # allows me to disable sending commands to aircon via UI.
      - condition: state
        entity_id: input_boolean.enable_aircon_controller
        state: "on"

      # send the climates current state to esphome.
      - service: esphome.bedroom_node_aircon_state
        data:
          temperature: "{{ state_attr('climate.bedroom_aircon', 'temperature') | int }}"
          operation_mode: "{{ states('climate.bedroom_aircon') }}"
          fan_mode: "{{ state_attr('climate.bedroom_aircon', 'fan_mode') }}"
          swing_mode: "{{ is_state_attr('climate.bedroom_aircon', 'swing_mode', 'on') }}"
          light: "{{ is_state('light.bedroom_aircon_light', 'on') }}"

      # could also send IR command via broadlink service calls etc.
```

### Example action to control existing Home Assistant devices

```yaml
climate:
  - platform: climate_template
    # ...
    set_hvac_mode:
      # allows you to control an existing Home Assistant HVAC device
      - service: climate.set_hvac_mode
        data:
          entity_id: climate.bedroom_ac_nottemplate
          hvac_mode: "{{ states('climate.bedroom_ac_template') }}"
```

### Example of using presets modes to control boiler with multiple heating modes with independent temperatures

```yaml
climate:
  - platform: climate_template
    name: "Heating Circuit 1"
    unique_id: "climate_template_heating_hc1"
    mode_action: "queued"
    max_action: 3
    # only heat mode is defined (no off mode), as boiler uses freeze 'protection' preset mode as off     
    hvac_modes:
      - "heat"
    # custom defined presets to match boiler mode
    preset_modes:
      - "automatic"
      - "comfort"
      - "reduced"
      - "protection"
    # active preset features set as bits: 1 (presets are editable via HA) + 2 (presets are saved and restore in HA) + 32 (preset allowed for target temperature) = 35
    presets_features: 35
    min_temp: 10
    max_temp: 30
    temp_step: 0.5
    # get current boiler target temperature
    current_temperature_template: "{{ states('sensor.boiler_hc1_room_temperature_actual_value') }}"
    # just to init default hvac mode (only 'heat' mode is used)
    hvac_mode_template: "heat"
    # get current active preset mode if changed on boiler controller
    preset_mode_template: "{{ states('select.boiler_hc1_operating_mode') | lower }}"
    # updates integration presets temperatures if changed on boiler controller
    presets_template: "{{ {'automatic': { 'target_temperature': states('number.boiler_hc1_room_temperature_comfort_setpoint')}, 'comfort': { 'target_temperature': states('number.boiler_hc1_room_temperature_comfort_setpoint')}, 'reduced': { 'target_temperature': states('number.boiler_hc1_room_temperature_reduced_setpoint')}, 'protection': { 'target_temperature': states('number.boiler_hc1_room_temperature_protection_setpoint')}} }}"
    hvac_action_template: "{% if 'Heating' in states('sensor.boiler_hc1_status') %}heating{% else %}idle{% endif %}"
    # updates boiler controller temperatures if changed via HomeAssistant
    set_presets:
      # set boiler comfort preset temperature
      - if:
          - condition: template
            value_template: "{{ ( 'automatic' in changed and 'target_temperature' in changed.automatic ) or ( 'comfort' in changed and 'target_temperature' in comfort.automatic ) }}"
        then:    
          - service: number.set_value
            target:
              entity_id: "number.boiler_hc1_room_temperature_comfort_setpoint"
            data:
              value: "{% if 'automatic' in changed and 'target_temperature' in changed.automatic %}{{ changed.automatic.target_temperature }}{% else %}{{ changed.automatic.target_temperature }}{% endif %}"
      # set boiler reduced preset temperature
      - if:
          - condition: template
            value_template: "{{ ( 'reduced' in changed and 'target_temperature' in reduced.automatic ) }}"
        then:
          - service: number.set_value
            target:
              entity_id: "number.boiler_hc1_room_temperature_reduced_setpoint"
            data:
              value: "{{ changed.reduced.target_temperature }}"
      # set boiler freeze protection temperature
      - if:
          - condition: template
            value_template: "{{ ( 'protection' in changed and 'target_temperature' in protection.automatic ) }}"
        then:
          - service: number.set_value
            target:
              entity_id: "number.boiler_hc1_room_temperature_protection_setpoint"
            data:
              value: "{{ changed.protection.target_temperature }}"
    # set boiler current preset mode
    set_preset_mode:
      - service: select.select_option
        target:
          entity_id: select.boiler_hc1_operating_mode
        data:
          option: "{{ preset_mode | title }}"
```




### Use Cases

- Merge multiple components into one climate device (just like any template platform).
- Control optimistic climate devices such as IR aircons via service calls.
