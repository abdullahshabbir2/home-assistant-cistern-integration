import async_timeout
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging

from .const import UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class CisternDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host: str, port: int):
        self._url = f"http://{host}:{port}"
        super().__init__(
            hass,
            _LOGGER,
            name="cistern",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from /status."""
        try:
            async with async_timeout.timeout(10):
                session = self.hass.helpers.aiohttp_client.async_get_clientsession()
                resp = await session.get(f"{self._url}/status")
                resp.raise_for_status()
                return await resp.json()
        except Exception as err:
            raise UpdateFailed(err)

    async def send_command(self, payload: dict):
        """POST to /command with a 10 s timeout, log errors, then refresh."""
        try:
            async with async_timeout.timeout(10):
                session = self.hass.helpers.aiohttp_client.async_get_clientsession()
                response = await session.post(f"{self._url}/command", json=payload)
                response.raise_for_status()
        except Exception as err:
            _LOGGER.error("Error sending command to %s: %s", self._url, err)
        finally:
            # Always refresh so the UI sees the updated state (or reverts if the POST failed)
            await self.async_request_refresh()
