from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo

from ..constants import *
from ..entity.DiagnosticSensor import DiagnosticSensor


class DiagnosticsEntry:
    def __init__(self, hass, entry):
        self._hass = hass
        self._entry = entry

    async def async_setup(self):
        await self._hass.data[DOMAIN][CONFIG_DIAGNOSTIC_COORDINATOR].async_refresh()
        await self._hass.config_entries.async_forward_entry_setups(self._entry, PLATFORMS)

        return True

    async def async_unload(self):
        await self._hass.config_entries.async_unload_platforms(self._entry, PLATFORMS)

        return True

    async def async_remove(self):
        pass

    async def async_setup_sensor(self, async_add_entities):
        deviceInfo = self._deviceInfo()
        diagnosticCoordinator = self._hass.data[DOMAIN][CONFIG_DIAGNOSTIC_COORDINATOR]

        async_add_entities([
            DiagnosticSensor('state', 'State', deviceInfo, diagnosticCoordinator),
            DiagnosticSensor('devices_healthy', 'Devices Healthy', deviceInfo, diagnosticCoordinator),
            DiagnosticSensor('devices_unhealthy', 'Devices Unhealthy', deviceInfo, diagnosticCoordinator),
            DiagnosticSensor('entities_healthy', 'Entities Healthy', deviceInfo, diagnosticCoordinator),
            DiagnosticSensor('entities_unhealthy', 'Entities Unhealthy', deviceInfo, diagnosticCoordinator),
        ])

    def _deviceInfo(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name='Template Device Diagnostics',
            model='Diagnostics',
            manufacturer=AUTHOR,
            sw_version=VERSION,
            entry_type=DeviceEntryType.SERVICE,
        )
