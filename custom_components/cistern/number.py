# config/custom_components/cistern/number.py

from homeassistant.components.number import NumberEntity
from .const import DOMAIN

# key → (label, min, max, step, parameter path)
FIELDS = {
    # 1) Global irrigation
    "irrigation_optimization_level": (
        "Irrigation Optimization Level", 0, 10, 1,
        ("irrigation",)
    ),
    "max_manual_irrigation_duration": (
        "Max Manual Irrigation Duration (min)", 0, 120, 1,
        ("irrigation",)
    ),

    # 2) Zone areas
    "irrigation_zone1_area": ("Zone 1 Area (sqm)", 0, 1000, 1, ("irrigation","zone_areas")),
    "irrigation_zone2_area": ("Zone 2 Area (sqm)", 0, 1000, 1, ("irrigation","zone_areas")),
    "irrigation_zone3_area": ("Zone 3 Area (sqm)", 0, 1000, 1, ("irrigation","zone_areas")),
    "irrigation_zone4_area": ("Zone 4 Area (sqm)", 0, 1000, 1, ("irrigation","zone_areas")),
    "irrigation_zone5_area": ("Zone 5 Area (sqm)", 0, 1000, 1, ("irrigation","zone_areas")),
    "irrigation_zone6_area": ("Zone 6 Area (sqm)", 0, 1000, 1, ("irrigation","zone_areas")),
    "irrigation_zone7_area": ("Zone 7 Area (sqm)", 0, 1000, 1, ("irrigation","zone_areas")),
    "irrigation_zone8_area": ("Zone 8 Area (sqm)", 0, 1000, 1, ("irrigation","zone_areas")),

    # 3) Zone manual override
    "irrigation_zone1_manual": ("Zone 1 Manual Override", 0, 1, 1, ("irrigation","zone_manual")),
    "irrigation_zone2_manual": ("Zone 2 Manual Override", 0, 1, 1, ("irrigation","zone_manual")),
    "irrigation_zone3_manual": ("Zone 3 Manual Override", 0, 1, 1, ("irrigation","zone_manual")),
    "irrigation_zone4_manual": ("Zone 4 Manual Override", 0, 1, 1, ("irrigation","zone_manual")),
    "irrigation_zone5_manual": ("Zone 5 Manual Override", 0, 1, 1, ("irrigation","zone_manual")),
    "irrigation_zone6_manual": ("Zone 6 Manual Override", 0, 1, 1, ("irrigation","zone_manual")),
    "irrigation_zone7_manual": ("Zone 7 Manual Override", 0, 1, 1, ("irrigation","zone_manual")),
    "irrigation_zone8_manual": ("Zone 8 Manual Override", 0, 1, 1, ("irrigation","zone_manual")),

    # 4) Zone optimization flags
    "irrigation_zone1_optimization_active": ("Zone 1 Optimization Active", 0, 1, 1, ("irrigation","zone_optimization")),
    "irrigation_zone2_optimization_active": ("Zone 2 Optimization Active", 0, 1, 1, ("irrigation","zone_optimization")),
    "irrigation_zone3_optimization_active": ("Zone 3 Optimization Active", 0, 1, 1, ("irrigation","zone_optimization")),
    "irrigation_zone4_optimization_active": ("Zone 4 Optimization Active", 0, 1, 1, ("irrigation","zone_optimization")),
    "irrigation_zone5_optimization_active": ("Zone 5 Optimization Active", 0, 1, 1, ("irrigation","zone_optimization")),
    "irrigation_zone6_optimization_active": ("Zone 6 Optimization Active", 0, 1, 1, ("irrigation","zone_optimization")),
    "irrigation_zone7_optimization_active": ("Zone 7 Optimization Active", 0, 1, 1, ("irrigation","zone_optimization")),
    "irrigation_zone8_optimization_active": ("Zone 8 Optimization Active", 0, 1, 1, ("irrigation","zone_optimization")),

    # 5) Zone demands
    "irrigation_zone1_demand_litres_per_sqm": ("Zone 1 Demand (L/m²)", 0, 500, 1, ("irrigation","zone_irrigation_demand")),
    "irrigation_zone2_demand_litres_per_sqm": ("Zone 2 Demand (L/m²)", 0, 500, 1, ("irrigation","zone_irrigation_demand")),
    "irrigation_zone3_demand_litres_per_sqm": ("Zone 3 Demand (L/m²)", 0, 500, 1, ("irrigation","zone_irrigation_demand")),
    "irrigation_zone4_demand_litres_per_sqm": ("Zone 4 Demand (L/m²)", 0, 500, 1, ("irrigation","zone_irrigation_demand")),
    "irrigation_zone5_demand_litres_per_sqm": ("Zone 5 Demand (L/m²)", 0, 500, 1, ("irrigation","zone_irrigation_demand")),
    "irrigation_zone6_demand_litres_per_sqm": ("Zone 6 Demand (L/m²)", 0, 500, 1, ("irrigation","zone_irrigation_demand")),
    "irrigation_zone7_demand_litres_per_sqm": ("Zone 7 Demand (L/m²)", 0, 500, 1, ("irrigation","zone_irrigation_demand")),
    "irrigation_zone8_demand_litres_per_sqm": ("Zone 8 Demand (L/m²)", 0, 500, 1, ("irrigation","zone_irrigation_demand")),

    # 6) Outlet functions
    "outlet_configuration_1": ("Outlet 1 Configuration", 0, 2, 1, ("outlet_functions",)),
    "outlet_configuration_2": ("Outlet 2 Configuration", 0, 2, 1, ("outlet_functions",)),
    "outlet_configuration_3": ("Outlet 3 Configuration", 0, 2, 1, ("outlet_functions",)),
    "outlet_configuration_4": ("Outlet 4 Configuration", 0, 2, 1, ("outlet_functions",)),
    "outlet_configuration_5": ("Outlet 5 Configuration", 0, 2, 1, ("outlet_functions",)),
    "outlet_configuration_6": ("Outlet 6 Configuration", 0, 2, 1, ("outlet_functions",)),
    "outlet_configuration_7": ("Outlet 7 Configuration", 0, 2, 1, ("outlet_functions",)),
    "outlet_configuration_8": ("Outlet 8 Configuration", 0, 2, 1, ("outlet_functions",)),

    # 7) Sensor thresholds & numeric flags
    "flow_sensor_max_volume":           ("Flow Sensor Max Volume",               0, 10000, 1, ("sensors",)),
    "level_controller_mode":            ("Level Controller Mode",               0,     2, 1, ("sensors",)),
    "lower_level_controller_threshold": ("Lower Level Controller Threshold",     0,   100, 1, ("sensors",)),
    "upper_level_controller_threshold": ("Upper Level Controller Threshold",     0,   100, 1, ("sensors",)),
    "warning_threshold":                ("Warning Threshold",                   0,   100, 1, ("sensors",)),

    # 8) Tank configuration
    "tank_pre_defined_model":           ("Tank Pre-Defined Model",              0,    10, 1, ("tank_configuration",)),
    "number_of_tanks":                  ("Number of Tanks",                     1,     4, 1, ("tank_configuration",)),
    "tank_measure_A_meters":            ("Tank Measure A (m)",                  0,    10, 0.1,("tank_configuration",)),
    "tank_measure_B_meters":            ("Tank Measure B (m)",                  0,    10, 0.1,("tank_configuration",)),
    "tank_measure_C_meters":            ("Tank Measure C (m)",                  0,    10, 0.1,("tank_configuration",)),
    "max_refill_duration_minutes":      ("Max Refill Duration (min)",           0,   120, 1, ("tank_configuration",)),
    "collection_surface_sqm":           ("Collection Surface (sqm)",            0,  1000, 1, ("tank_configuration",)),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coord = hass.data[DOMAIN][entry.entry_id]
    entities = [
        CisternNumber(coord, key, label, minv, maxv, step, path)
        for key, (label, minv, maxv, step, path) in FIELDS.items()
    ]
    async_add_entities(entities)

class CisternNumber(NumberEntity):
    def __init__(self, coord, key, name, minv, maxv, step, param_path):
        self.coordinator = coord
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{coord._url}_{key}"
        self._attr_min_value = minv
        self._attr_max_value = maxv
        self._attr_step = step
        self._attr_mode = "slider"
        self._param_path = param_path

    @property
    def value(self):
        return self.coordinator.data.get(self.key)

    @property
    def available(self):
        return self.coordinator.last_update_success

    async def async_set_value(self, value: float) -> None:
        # Build nested parameters dict
        params = {}
        d = params
        for p in self._param_path:
            d[p] = {}
            d = d[p]
        # Cast to int if necessary
        if isinstance(value, float) and value.is_integer():
            d[self.key] = int(value)
        else:
            d[self.key] = value

        await self.coordinator.send_command({
            "command": "update_device",
            "parameters": params
        })
