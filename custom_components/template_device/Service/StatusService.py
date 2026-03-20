from ..Constants import *


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
        config = self._hass.data[DOMAIN]

        return config[CONFIG_ASSIGN_MANAGER].status()
