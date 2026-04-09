"""ESP32 Cistern integration: setup, teardown, and device registration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, UPDATE_INTERVAL
from .coordinator import CisternDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# Added "time" so HA picks up time.py
PLATFORMS = ["sensor", "switch", "number", "time"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Cistern from a config entry."""
    host = entry.data["host"]
    port = entry.data["port"]

    # Create the coordinator and do first data fetch
    coordinator = CisternDataUpdateCoordinator(hass, host, port)
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator so platforms can access it
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Register a Device in Home Assistant
    dr.async_get(hass).async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, host)},
        manufacturer="DIY",
        model="ESP32 Cistern",
        name=f"Cistern @{host}",
    )

    # Forward setup to each platform
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    _LOGGER.debug("Cistern integration set up for %s:%s", host, port)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and all its platforms."""
    # Unload each platform and collect results
    unload_results = [
        await hass.config_entries.async_forward_entry_unload(entry, platform)
        for platform in PLATFORMS
    ]
    unload_ok = all(unload_results)

    if unload_ok:
        # Remove the coordinator
        hass.data[DOMAIN].pop(entry.entry_id)

    _LOGGER.debug("Cistern integration unloaded: %s", entry.entry_id)
    return unload_ok
