from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SENSORS = {
  "device_id":                     ("Device ID", None),
  "device_name":                   ("Device Name", None),
  "serial_number":                 ("Serial Number", None),
  "ip_address":                    ("IP Address", None),
  "mac_address":                   ("MAC Address", None),
  "connected_to_network":          ("SSID", None),
  "fill_level_percent":            ("Fill Level %", "%"),
  "fill_level_liter":              ("Fill Level L", "L"),
  "fill_level_height":             ("Fill Height (m)", "m"),
  **{f"outlet_configuration_{i}": (f"Outlet Config {i}", None) for i in range(1,9)},
  "filter_status":                 ("Filter Status", None),
  "extraction_pumps_active":       ("Extraction Pumps Active", None),
  "time_controlled_outlets_active":("Time-Ctrl Outlets Active", None),
  "refill_appliances_active":      ("Refill Appliances Active", None),
  "drainage_appliances_active":    ("Drainage Appliances Active", None),
  "filter_check_appliances_active":("Filter-Check Appliances Active", None),
  "irrigation_valves_active":      ("Irrigation Valves Active", None),
  "expected_precipitation_litres_per_sqm": ("Expected Precip (L/m²)", None),
  "historic_precipitation_litres_per_sqm": ("Historic Precip (L/m²)", None),
  "expected_inflow_litres":        ("Expected Inflow (L)", "L"),
  **{f"planned_irrigation_start_zone{i}": (f"Planned Zone {i} Start", None) for i in range(1,9)},
  **{f"planned_irrigation_end_zone{i}":   (f"Planned Zone {i} End",   None) for i in range(1,9)},
  "operating_mode":                ("Operating Mode", None),
  "error":                         ("Error", None),
  "timestamp":                     ("Last Update", None),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    entities = [
        SensorEntityWrapper(coord, key, name, unit)
        for key, (name, unit) in SENSORS.items()
    ]
    async_add_entities(entities)

class SensorEntityWrapper(SensorEntity):
    def __init__(self, coord, key, name, unit):
        self.coord = coord
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{coord._url}_{key}"
        if unit:
            self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self):
        return self.coord.data.get(self.key)

    @property
    def available(self):
        return self.coord.last_update_success
