from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory

from ..Constants import DOMAIN


class StateSensor(SensorEntity):
    def __init__(self, internalName, deviceInfo):
        self._isRegistered = False

        self._entityId = f"{internalName}_state"
        self._entityName = 'state'
        self._entityLabel = 'State'
        self._attr_unique_id = f"{DOMAIN}_{self._entityId}"
        self._attr_device_info = deviceInfo
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self):
        return self._entityLabel if self._isRegistered else self._entityId

    @property
    def native_value(self):
        return 'ok'

    async def async_added_to_hass(self):
        self._isRegistered = True

    async def async_will_remove_from_hass(self):
        self._isRegistered = False
