from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..constants import DOMAIN


class DiagnosticSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, key, name, prefix, deviceInfo, diagnosticCoordinator):
        super().__init__(diagnosticCoordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{prefix}_{key}"
        self._attr_suggested_object_id = self._attr_unique_id
        self._attr_device_info = deviceInfo
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key) if isinstance(self.coordinator.data, dict) else None
