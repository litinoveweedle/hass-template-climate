"""Template listener lifecycle tests (cold start, reload, restore)."""

import copy
from unittest.mock import patch

from homeassistant import config as config_util
from homeassistant.components.climate.const import (
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    EVENT_HOMEASSISTANT_START,
    EVENT_STATE_CHANGED,
)
from homeassistant.core import CoreState, HomeAssistant, State
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import mock_restore_cache

ENTITY_ID = "climate.template_climate_listener_test"
SOURCE = "sensor.test_temperature"
SOURCE_2 = "sensor.test_temperature_2"

CONFIG = {
    "climate": [
        {
            "platform": "climate_template",
            "name": "Template Climate Listener Test",
            "unique_id": "template_climate_listener_test",
            "hvac_modes": ["off"],
            "current_temperature_template": "{{ states('%s') }}" % SOURCE,
        }
    ]
}


async def _setup(hass: HomeAssistant, config: dict = CONFIG) -> None:
    assert await async_setup_component(hass, "climate", config)
    await hass.async_block_till_done()


async def _reload(hass: HomeAssistant, config: dict = CONFIG) -> None:
    with patch.object(
        config_util, "load_yaml_config_file", return_value=copy.deepcopy(config)
    ):
        await hass.services.async_call("climate_template", "reload", blocking=True)
    await hass.async_block_till_done()


async def _set_source(hass: HomeAssistant, value: str, entity: str = SOURCE) -> None:
    hass.states.async_set(entity, value)
    await hass.async_block_till_done()


def _temp(hass: HomeAssistant):
    state = hass.states.get(ENTITY_ID)
    assert state is not None
    return state.attributes.get("current_temperature")


async def test_target_temperature_attributes_follow_hvac_mode(
    hass: HomeAssistant,
) -> None:
    """Only expose the target fields matching the active HVAC mode."""
    entity_id = "climate.template_climate_target_mode_test"
    config = {
        "climate": [
            {
                "platform": "climate_template",
                "name": "Template Climate Target Mode Test",
                "unique_id": "template_climate_target_mode_test",
                "hvac_modes": ["off", "heat", "heat_cool"],
                "target_temperature_template": "21",
                "target_temperature_low_template": "17",
                "target_temperature_high_template": "22",
            }
        ]
    }
    await _setup(hass, config)

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.attributes.get(ATTR_TEMPERATURE) == 21
    assert state.attributes.get(ATTR_TARGET_TEMP_LOW) is None
    assert state.attributes.get(ATTR_TARGET_TEMP_HIGH) is None

    await hass.services.async_call(
        "climate",
        "set_hvac_mode",
        {"entity_id": entity_id, "hvac_mode": "heat_cool"},
        blocking=True,
    )
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.attributes.get(ATTR_TEMPERATURE) is None
    assert state.attributes.get(ATTR_TARGET_TEMP_LOW) == 17
    assert state.attributes.get(ATTR_TARGET_TEMP_HIGH) == 22

    await hass.services.async_call(
        "climate",
        "set_hvac_mode",
        {"entity_id": entity_id, "hvac_mode": "heat"},
        blocking=True,
    )
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.attributes.get(ATTR_TEMPERATURE) == 21
    assert state.attributes.get(ATTR_TARGET_TEMP_LOW) is None
    assert state.attributes.get(ATTR_TARGET_TEMP_HIGH) is None


async def test_initial_render_and_follow(hass: HomeAssistant) -> None:
    """Entity renders the source on setup and follows later changes."""
    hass.states.async_set(SOURCE, "20")
    await _setup(hass)
    assert _temp(hass) == 20

    await _set_source(hass, "22.5")
    assert _temp(hass) == 22.5


async def test_cold_start_tracks_after_homeassistant_start(
    hass: HomeAssistant,
) -> None:
    """Tracking starts once HA has started when set up before startup."""
    hass.set_state(CoreState.not_running)
    hass.states.async_set(SOURCE, "19")
    await _setup(hass)

    hass.bus.async_fire(EVENT_HOMEASSISTANT_START)
    hass.set_state(CoreState.running)
    await hass.async_block_till_done()
    assert _temp(hass) == 19

    await _set_source(hass, "21")
    assert _temp(hass) == 21


async def test_reload_while_running_renders_and_follows(hass: HomeAssistant) -> None:
    """After reload in a running HA the entity renders and keeps following."""
    hass.states.async_set(SOURCE, "20")
    await _setup(hass)

    await _set_source(hass, "23")
    await _reload(hass)
    assert hass.states.get(ENTITY_ID) is not None
    assert _temp(hass) == 23

    await _set_source(hass, "24")
    assert _temp(hass) == 24


async def test_repeated_reloads_keep_following(hass: HomeAssistant) -> None:
    """Every reload re-establishes tracking."""
    hass.states.async_set(SOURCE, "20")
    await _setup(hass)

    for value in ("21", "22", "23"):
        await _reload(hass)
        await _set_source(hass, value)
        assert _temp(hass) == int(value)


async def test_reload_cleans_up_old_listeners(hass: HomeAssistant) -> None:
    """One source change yields exactly one state update after many reloads."""
    hass.states.async_set(SOURCE, "20")
    await _setup(hass)
    for _ in range(3):
        await _reload(hass)

    events = []
    hass.bus.async_listen(
        EVENT_STATE_CHANGED,
        lambda event: (
            events.append(event) if event.data["entity_id"] == ENTITY_ID else None
        ),
    )

    await _set_source(hass, "27")
    assert _temp(hass) == 27
    updates = [
        e
        for e in events
        if e.data["new_state"]
        and e.data["new_state"].attributes.get("current_temperature") == 27
    ]
    assert len(updates) == 1
    assert len([s for s in hass.states.async_all("climate")]) == 1


async def test_reload_with_changed_source_template(hass: HomeAssistant) -> None:
    """A changed template in YAML is used after reload."""
    hass.states.async_set(SOURCE, "20")
    hass.states.async_set(SOURCE_2, "15")
    await _setup(hass)

    new_config = copy.deepcopy(CONFIG)
    new_config["climate"][0]["current_temperature_template"] = (
        "{{ states('%s') }}" % SOURCE_2
    )
    await _reload(hass, new_config)
    assert _temp(hass) == 15

    await _set_source(hass, "16", SOURCE_2)
    assert _temp(hass) == 16

    await _set_source(hass, "30", SOURCE)
    assert _temp(hass) == 16


async def test_update_entity_after_reload(hass: HomeAssistant) -> None:
    """homeassistant.update_entity works after reload (tracker exists)."""
    hass.states.async_set(SOURCE, "20")
    assert await async_setup_component(hass, "homeassistant", {})
    await _setup(hass)
    await _reload(hass)
    await _set_source(hass, "25")

    await hass.services.async_call(
        "homeassistant", "update_entity", {"entity_id": ENTITY_ID}, blocking=True
    )
    await hass.async_block_till_done()
    assert _temp(hass) == 25


async def test_restored_value_overwritten_by_render(hass: HomeAssistant) -> None:
    """A rendered value wins over the restored one, on setup and reload."""
    mock_restore_cache(hass, [State(ENTITY_ID, "off", {"current_temperature": 18})])
    hass.states.async_set(SOURCE, "21")
    await _setup(hass)
    assert _temp(hass) == 21

    await _set_source(hass, "22")
    await _reload(hass)
    assert _temp(hass) == 22


async def test_restored_zero_temperature_overwritten(hass: HomeAssistant) -> None:
    """A restored 0 is a valid value and is replaced by the render."""
    mock_restore_cache(hass, [State(ENTITY_ID, "off", {"current_temperature": 0})])
    hass.states.async_set(SOURCE, "17")
    await _setup(hass)
    assert _temp(hass) == 17


async def test_restored_zero_kept_without_template(hass: HomeAssistant) -> None:
    """Without a temperature template the restored 0 is preserved."""
    mock_restore_cache(hass, [State(ENTITY_ID, "off", {"current_temperature": 0})])
    config = copy.deepcopy(CONFIG)
    del config["climate"][0]["current_temperature_template"]
    await _setup(hass, config)
    assert _temp(hass) == 0


async def test_no_restored_state(hass: HomeAssistant) -> None:
    """Without restored state the template still drives the value."""
    hass.states.async_set(SOURCE, "18")
    await _setup(hass)
    assert _temp(hass) == 18
