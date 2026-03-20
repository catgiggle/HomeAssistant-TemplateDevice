from datetime import datetime

from homeassistant.helpers import entity_registry, device_registry

from ..Constants import *
from ..Utils.Database import Database


class AssignManager:
    def __init__(self, hass, storagePath):
        self._hass = hass
        self._storagePath = storagePath

    def assign(self, entityId, deviceId):
        self._storeInRegistry(entityId, deviceId)
        self._storeInDatabase(entityId, deviceId)

    def unassign(self, entityId):
        self._deleteFromRegistry(entityId)
        self._deleteFromDatabase(entityId)

    def reload(self):
        for deviceId, deviceEntities in self._getAssignments().items():
            for entityId in deviceEntities:
                self._storeInRegistry(entityId, deviceId)

    def status(self):
        result = {}

        deviceRegistry = device_registry.async_get(self._hass)
        entityRegistry = entity_registry.async_get(self._hass)

        for deviceId, deviceEntities in self._getAssignments().items():
            deviceEntry = deviceRegistry.async_get(deviceId)

            if deviceEntry is None:
                result[deviceId] = 'unavailable'
                continue

            result[deviceId] = {
                entityId: 'ok' if entityRegistry.async_get(entityId) else 'unavailable'
                for entityId in deviceEntities
            }

        return result

    def _getAssignments(self):
        result = {}

        with Database.connect(self._storagePath) as connection:
            for deviceId, entityId in connection.execute('SELECT deviceId, entityId FROM assignments ORDER BY deviceId, entityId').fetchall():
                result.setdefault(deviceId, []).append(entityId)

        return result

    def _storeInDatabase(self, entityId, deviceId):
        now = datetime.now().strftime(DATETIME_FORMAT)

        with Database.connect(self._storagePath) as connection:
            connection.execute('''
                INSERT INTO assignments (entityId, deviceId, createdAt, modifiedAt)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(entityId) DO UPDATE SET
                    deviceId = excluded.deviceId,
                    modifiedAt = excluded.modifiedAt
            ''', (entityId, deviceId, now, now))

    def _deleteFromDatabase(self, entityId):
        with Database.connect(self._storagePath) as connection:
            connection.execute('DELETE FROM assignments WHERE 1', (entityId,))

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

    def _deleteFromRegistry(self, entityId):
        entityRegistry = entity_registry.async_get(self._hass)
        entityEntry = entityRegistry.async_get(entityId)

        if entityEntry is None:
            return False

        entityRegistry.async_update_entity(entity_id=entityEntry.entity_id, device_id=None)

        return True
