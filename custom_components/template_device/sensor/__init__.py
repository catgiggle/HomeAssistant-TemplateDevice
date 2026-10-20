from homeassistant.helpers.device_registry import DeviceInfo

from .DiagnosticSensor import DiagnosticSensor
from ..constants import *


async def async_setup_entry(hass, entry, async_add_entities):
    config = hass.data[DOMAIN][entry.entry_id]
    prefix = config[CONFIG_INTERNAL_NAME]
    deviceInfo = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=config[CONFIG_DISPLAY_NAME],
        model=NAME,
        serial_number=prefix,
        manufacturer=AUTHOR,
        sw_version=VERSION,
    )
    diagnosticCoordinator = hass.data[DOMAIN][CONFIG_DIAGNOSTIC_COORDINATOR]

    async_add_entities([
        DiagnosticSensor('state', 'State', prefix, deviceInfo, diagnosticCoordinator),
        DiagnosticSensor('devices_healthy', 'Devices Healthy', prefix, deviceInfo, diagnosticCoordinator),
        DiagnosticSensor('devices_unhealthy', 'Devices Unhealthy', prefix, deviceInfo, diagnosticCoordinator),
        DiagnosticSensor('entities_healthy', 'Entities Healthy', prefix, deviceInfo, diagnosticCoordinator),
        DiagnosticSensor('entities_unhealthy', 'Entities Unhealthy', prefix, deviceInfo, diagnosticCoordinator),
    ])
