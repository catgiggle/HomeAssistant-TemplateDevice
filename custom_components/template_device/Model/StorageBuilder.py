import os

from custom_components.template_device.Utils.Database import Database


class StorageBuilder:
    def __init__(self, storagePath):
        self._storagePath = storagePath

    def build(self):
        os.makedirs(os.path.dirname(self._storagePath), exist_ok=True)

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
