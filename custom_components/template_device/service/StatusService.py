from ..constants import *


class StatusService:
    def __init__(self, hass):
        self._hass = hass

    def register(self):
        self._hass.services.async_register(
            DOMAIN,
            'status',
            self.handle,
            supports_response=True
        )

    async def handle(self, _request):
        return await self._hass.data[DOMAIN][CONFIG_ASSIGN_MANAGER].async_status()
