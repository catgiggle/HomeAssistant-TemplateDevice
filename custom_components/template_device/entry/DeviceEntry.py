from homeassistant.helpers import device_registry
from homeassistant.helpers.device_registry import DeviceInfo

from ..constants import *
from ..entity.DeviceSensor import DeviceSensor


class DeviceEntry:
    def __init__(self, hass, entry):
        self._hass = hass
        self._entry = entry

    async def async_setup(self):
        await self._hass.config_entries.async_forward_entry_setups(self._entry, PLATFORMS)
        await self._deviceAction('async_device_setup')

        return True

    async def async_unload(self):
        await self._hass.config_entries.async_unload_platforms(self._entry, PLATFORMS)
        await self._deviceAction('async_device_unload')

        return True

    async def async_remove(self):
        await self._deviceAction('async_device_cleanup')

    async def async_setup_sensor(self, async_add_entities):
        async_add_entities([
            DeviceSensor(
                self._entry.data.get(CONFIG_INTERNAL_NAME),
                DeviceInfo(
                    identifiers={(DOMAIN, self._entry.entry_id)},
                    name=self._entry.data.get(CONFIG_DISPLAY_NAME),
                    model=NAME,
                    serial_number=self._entry.data.get(CONFIG_INTERNAL_NAME),
                    manufacturer=AUTHOR,
                    sw_version=VERSION,
                )
            ),
        ])

    async def _deviceAction(self, method_name):
        registry = device_registry.async_get(self._hass)
        device = registry.async_get_device(identifiers={(DOMAIN, self._entry.entry_id)})

        if device:
            config = self._hass.data.get(DOMAIN)
            assignManager = config[CONFIG_ASSIGN_MANAGER]
            diagnosticCoordinator = config[CONFIG_DIAGNOSTIC_COORDINATOR]

            await getattr(assignManager, method_name)(device.id)
            await diagnosticCoordinator.async_request_refresh()
