import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from ..constants import *


class UnassignService:
    def __init__(self, hass):
        self._hass = hass

    def register(self):
        self._hass.services.async_register(
            DOMAIN,
            'unassign',
            self.handle,
            schema=vol.Schema({
                vol.Required(FIELD_ENTITY_ID): cv.entity_ids,
            }),
        )

    async def handle(self, request):
        await self._hass.data[DOMAIN][CONFIG_ASSIGN_MANAGER].async_entity_unassign(
            request.data.get(FIELD_ENTITY_ID)
        )
