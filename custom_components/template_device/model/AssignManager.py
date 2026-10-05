from datetime import datetime

from homeassistant.helpers import entity_registry, device_registry

from ..constants import *
from ..utils.Database import Database


class AssignManager:
    def __init__(self, hass, storagePath):
        self._hass = hass
        self._storagePath = storagePath

    async def async_entity_assign(self, entityIds, deviceId):
        if isinstance(entityIds, str):
            entityIds = [entityIds]

        for entityId in entityIds:
            self._storeInRegistry(entityId, deviceId)

        await self._hass.async_add_executor_job(
            self._storeInDatabase, entityIds, deviceId
        )

    async def async_entity_unassign(self, entityIds):
        if isinstance(entityIds, str):
            entityIds = [entityIds]

        for entityId in entityIds:
            self._deleteFromRegistry(entityId)

        await self._hass.async_add_executor_job(
            self._deleteFromDatabase, entityIds
        )

    async def async_device_unload(self, deviceId):
        assignedEntityIds = await self._hass.async_add_executor_job(
            self._getAssignmentsForDevice, deviceId
        )

        if not assignedEntityIds:
            return

        for entityId in assignedEntityIds:
            self._deleteFromRegistry(entityId, deviceId)

    async def async_device_cleanup(self, deviceId):
        assignedEntityIds = await self._hass.async_add_executor_job(
            self._getAssignmentsForDevice, deviceId
        )

        if not assignedEntityIds:
            return

        await self.async_entity_unassign(assignedEntityIds)

    async def async_device_setup(self, deviceId):
        assignedEntityIds = await self._hass.async_add_executor_job(
            self._getAssignmentsForDevice, deviceId
        )

        for entityId in assignedEntityIds:
            self._storeInRegistry(entityId, deviceId)

    async def async_status(self):
        result = {}

        deviceRegistry = device_registry.async_get(self._hass)
        entityRegistry = entity_registry.async_get(self._hass)

        assignments = await self._hass.async_add_executor_job(
            self._getAssignmentsAll
        )

        for deviceId, deviceEntities in assignments.items():
            deviceEntry = deviceRegistry.async_get(deviceId)

            if deviceEntry is None:
                result[deviceId] = 'unavailable'
                continue

            result[deviceId] = {
                entityId: 'ok' if entityRegistry.async_get(entityId) else 'unavailable'
                for entityId in deviceEntities
            }

        return result

    def _getAssignmentsAll(self):
        result = {}

        with Database.connect(self._storagePath) as connection:
            assignments = connection.execute(
                'SELECT deviceId, entityId FROM assignments ORDER BY deviceId, entityId'
            ).fetchall()

            for deviceId, entityId in assignments:
                result.setdefault(deviceId, []).append(entityId)

        return result

    def _getAssignmentsForDevice(self, deviceId):
        with Database.connect(self._storagePath) as connection:
            assignments = connection.execute(
                'SELECT entityId FROM assignments WHERE deviceId = ?', (deviceId,)
            ).fetchall()

            return [entityId for (entityId,) in assignments]

    def _storeInDatabase(self, entityIds, deviceId):
        if isinstance(entityIds, str):
            entityIds = [entityIds]

        now = datetime.now().strftime(DATETIME_FORMAT)

        with Database.connect(self._storagePath) as connection:
            connection.executemany('''
                INSERT INTO assignments (entityId, deviceId, createdAt, modifiedAt)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(entityId) DO UPDATE SET
                    deviceId = excluded.deviceId,
                    modifiedAt = excluded.modifiedAt
            ''', [(entityId, deviceId, now, now) for entityId in entityIds])

    def _deleteFromDatabase(self, entityIds):
        if isinstance(entityIds, str):
            entityIds = [entityIds]

        with Database.connect(self._storagePath) as connection:
            connection.executemany(
                'DELETE FROM assignments WHERE entityId = ?',
                [(entityId,) for entityId in entityIds],
            )

    def _storeInRegistry(self, entityId, deviceId):
        deviceRegistry = device_registry.async_get(self._hass)
        deviceEntry = deviceRegistry.async_get(deviceId)

        if deviceEntry is None:
            return False

        entityRegistry = entity_registry.async_get(self._hass)
        entityEntry = entityRegistry.async_get(entityId)

        if entityEntry is None:
            return False

        entityRegistry.async_update_entity(entity_id=entityEntry.entity_id, device_id=deviceEntry.id)

        return True

    def _deleteFromRegistry(self, entityId, deviceId=None):
        entityRegistry = entity_registry.async_get(self._hass)
        entityEntry = entityRegistry.async_get(entityId)

        if entityEntry is None:
            return False

        if deviceId is not None and entityEntry.device_id != deviceId:
            return False

        entityRegistry.async_update_entity(entity_id=entityEntry.entity_id, device_id=None)

        return True
