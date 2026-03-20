import sqlite3
from contextlib import contextmanager


class Database:
    @staticmethod
    @contextmanager
    def connect(path):
        connection = sqlite3.connect(path)

        try:
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
