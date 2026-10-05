from pathlib import Path

from ..utils.Database import Database


class StorageBuilder:
    def __init__(self, hass, storagePath):
        self._hass = hass
        self._storagePath = Path(storagePath)

    async def async_build(self):
        await self._hass.async_add_executor_job(self._build)

    def _build(self):
        self._storagePath.parent.mkdir(parents=True, exist_ok=True)

        with Database.connect(self._storagePath) as connection:
            connection.execute('''
                CREATE TABLE IF NOT EXISTS assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entityId TEXT NOT NULL UNIQUE,
                    deviceId TEXT NOT NULL,
                    createdAt DATETIME NOT NULL,
                    modifiedAt DATETIME NOT NULL
                )
            ''')
