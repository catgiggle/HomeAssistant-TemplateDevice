from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory

from ..constants import DOMAIN


class StateSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = 'State'

    def __init__(self, internalName, deviceInfo):
        self._attr_unique_id = f"{DOMAIN}_{internalName}_state"
        self._attr_suggested_object_id = self._attr_unique_id
        self._attr_device_info = deviceInfo
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        return 'ok'
