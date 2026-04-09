from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    entities = []
    # Relay controls 1–8
    for i in range(1, 9):
        entities.append(CisternSwitch(coord,
            key=f"relay_control_{i}",
            name=f"Relay {i}"
        ))
    # Your other flag‐switches:
    for key, name in [
        ("filter_sensor_active", "Filter Sensor"),
        ("flow_manual_definition", "Flow Manual"),
        ("flow_sensor_active", "Flow Sensor"),
        ("level_sensor_active", "Level Sensor"),
        ("manual_tank_form_definition", "Manual Tank Def"),
        ("split_irrigation", "Split Irrigation"),
        ("switch_time_controlled_outlets", "Time-Ctrl Outlets"),
    ]:
        entities.append(CisternSwitch(coord, key=key, name=name))

    async_add_entities(entities)

class CisternSwitch(SwitchEntity):
    def __init__(self, coordinator, key: str, name: str):
        self.coordinator = coordinator
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator._url}_{key}"
        # **Optimistic** settings:
        self._attr_should_poll = False
        self._attr_assumed_state = True
        # initialize from last known data
        self._state = bool(self.coordinator.data.get(self.key))

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_turn_on(self, **kwargs):
        # 1) Flip state immediately in HA
        self._state = True
        self.async_write_ha_state()
        # 2) Send the real command
        await self.coordinator.send_command({
            "command": "update_device",
            "parameters": {self.key: 1}
        })

    async def async_turn_off(self, **kwargs):
        self._state = False
        self.async_write_ha_state()
        await self.coordinator.send_command({
            "command": "update_device",
            "parameters": {self.key: 0}
        })
