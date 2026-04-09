import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_PORT

DATA_SCHEMA = vol.Schema({
    vol.Required("host"): str,
    vol.Optional("port", default=DEFAULT_PORT): int,
})

class CisternFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ESP32 Cistern."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step (manual)."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

        host = user_input["host"]
        port = user_input["port"]
        # Create a unique ID for this device
        unique_id = f"{host}:{port}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return await self._test_and_create(user_input)

    async def async_step_zeroconf(self, discovery_info):
        """Handle zeroconf discovery (_cistern._tcp.local.)."""
        host = discovery_info.host
        port = int(discovery_info.port)

        unique_id = f"{host}:{port}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return await self._test_and_create({"host": host, "port": port})

    async def _test_and_create(self, data):
        """Test connectivity and create the config entry."""
        host = data["host"]
        port = data["port"]
        url = f"http://{host}:{port}/status"
        try:
            session = self.hass.helpers.aiohttp_client.async_get_clientsession()
            resp = await session.get(url, timeout=5)
            resp.raise_for_status()
            # Optionally validate JSON keys here…
            await resp.json()
        except Exception:
            return self.async_show_form(
                step_id="user",
                data_schema=DATA_SCHEMA,
                errors={"host": "cannot_connect"},
            )

        return self.async_create_entry(
            title=f"Cistern @ {host}",
            data=data
        )
