# config/custom_components/cistern/time.py

import datetime
from homeassistant.components.time import TimeEntity
from .const import DOMAIN

# Only the two global irrigation start times
TIME_FIELDS = {
    "irrigation_start_time_one": "Irrigation Start Time 1",
    "irrigation_start_time_two": "Irrigation Start Time 2",
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up time picker entities for the two global irrigation start times."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [
        CisternTime(coordinator, key, name)
        for key, name in TIME_FIELDS.items()
    ]
    async_add_entities(entities)

class CisternTime(TimeEntity):
    """TimeEntity for a global irrigation start time (HH:MM)."""

    def __init__(self, coordinator, key, name):
        self.coordinator = coordinator
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator._url}_{key}"

    @property
    def native_value(self) -> datetime.time | None:
        """Return the current time as a datetime.time object, parsed from "HH:MM"."""
        val = self.coordinator.data.get(self.key)
        if not isinstance(val, str):
            return None
        try:
            return datetime.datetime.strptime(val, "%H:%M").time()
        except ValueError:
            return None

    async def async_set_value(self, value: datetime.time) -> None:
        """When the user picks a new time, send the full HH:MM string."""
        time_str = value.strftime("%H:%M")
        await self.coordinator.send_command({
            "command": "update_device",
            "parameters": {
                "irrigation": {
                    self.key: time_str
                }
            }
        })
