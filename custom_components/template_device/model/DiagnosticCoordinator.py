from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..constants import DOMAIN

_LOGGER = logging.getLogger(__name__)


class DiagnosticCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, assignManager):
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=10),
        )
        self.assignManager = assignManager

    async def _async_update_data(self):
        status = await self.assignManager.async_status()
        devicesHealthy = 0
        devicesUnhealthy = 0
        entitiesHealthy = 0
        entitiesUnhealthy = 0

        for entities in status.values():
            if entities == 'unavailable':
                devicesUnhealthy += 1
            else:
                devicesHealthy += 1

                if isinstance(entities, dict):
                    for state in entities.values():
                        if state == 'ok':
                            entitiesHealthy += 1
                        else:
                            entitiesUnhealthy += 1

        return {
            'state': 'healthy' if (devicesUnhealthy == 0 and entitiesUnhealthy == 0) else 'unhealthy',
            'devices_healthy': devicesHealthy,
            'devices_unhealthy': devicesUnhealthy,
            'entities_healthy': entitiesHealthy,
            'entities_unhealthy': entitiesUnhealthy,
        }
