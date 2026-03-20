import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from ..Constants import *


class AssignService:
    def __init__(self, hass):
        self._hass = hass

    def register(self):
        self._hass.services.async_register(
            DOMAIN,
            'assign',
            self.handle,
            vol.Schema({
                vol.Required('entity_id'): cv.string,
                vol.Required('device_id'): cv.string,
            }, extra=vol.ALLOW_EXTRA),
        )

    async def handle(self, request):
        data = dict(request.data)
        config = self._hass.data[DOMAIN]
        config[CONFIG_ASSIGN_MANAGER].assign(data.get('entity_id'), data.get('device_id'))
