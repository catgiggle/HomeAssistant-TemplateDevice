import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from ..constants import *


class ClearService:
    def __init__(self, hass):
        self._hass = hass

    def register(self):
        self._hass.services.async_register(
            DOMAIN,
            'clear',
            self.handle,
            schema=vol.Schema({
                vol.Required(FIELD_DEVICE_ID): cv.string,
            }),
        )

    async def handle(self, request):
        await self._hass.data[DOMAIN][CONFIG_ASSIGN_MANAGER].async_device_cleanup(
            request.data.get(FIELD_DEVICE_ID)
        )
