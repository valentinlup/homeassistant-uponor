from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, SIGNAL_UPONOR_STATE_UPDATE

async def async_setup_entry(hass, entry, async_add_entities):
    state_proxy = hass.data[DOMAIN]["state_proxy"]

    entities = []
    for thermostat in hass.data[DOMAIN]["thermostats"]:
        if state_proxy.has_floor_temperature(thermostat):
            entities.append(UponorFloorTemperatureSensor(state_proxy, thermostat))
            entities.append(UponorHumiditySensor(state_proxy, thermostat))
    
    async_add_entities(entities, update_before_add=False)

class UponorFloorTemperatureSensor(SensorEntity):
    def __init__(self, state_proxy, thermostat):
        self._state_proxy = state_proxy
        self._thermostat = thermostat
        self._attr_name = f"{state_proxy.get_room_name(thermostat)} Floor Temperature"
        self._attr_unique_id = f"{state_proxy.get_thermostat_id(thermostat)}_floor_temp"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._state_proxy.get_thermostat_id(self._thermostat))},
            "name": self._state_proxy.get_room_name(self._thermostat),
            "manufacturer": "Uponor",
            "model": self._state_proxy.get_model(),
            "sw_version": self._state_proxy.get_version(self._thermostat)
        }

    @property
    def native_value(self):
        return self._state_proxy.get_floor_temperature(self._thermostat)

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_UPONOR_STATE_UPDATE, self._update_callback
            )
        )

    @callback
    def _update_callback(self):
        self.async_write_ha_state()

class UponorHumiditySensor(SensorEntity):
    def __init__(self, state_proxy, thermostat):
        self._state_proxy = state_proxy
        self._thermostat = thermostat
        self._attr_name = f"{state_proxy.get_room_name(thermostat)} humidity"
        self._attr_unique_id = f"{state_proxy.get_thermostat_id(thermostat)}_rh"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._state_proxy.get_thermostat_id(self._thermostat))},
            "name": self._state_proxy.get_room_name(self._thermostat),
            "manufacturer": "Uponor",
            "model": self._state_proxy.get_model(),
            "sw_version": self._state_proxy.get_version(self._thermostat)
        }

    @property
    def native_value(self):
        return self._state_proxy.get_floor_temperature(self._thermostat)

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_UPONOR_STATE_UPDATE, self._update_callback
            )
        )

    @callback
    def _update_callback(self):
        self.async_write_ha_state()