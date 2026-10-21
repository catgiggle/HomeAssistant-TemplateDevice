from homeassistant.components.sensor import SensorEntity

from ..constants import DOMAIN


class DeviceSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, prefix, deviceInfo):
        self._attr_name = 'State'
        self._attr_unique_id = f"{DOMAIN}_{prefix}_state"
        self._attr_suggested_object_id = self._attr_unique_id
        self._attr_device_info = deviceInfo
        self._attr_native_value = 'ok'
