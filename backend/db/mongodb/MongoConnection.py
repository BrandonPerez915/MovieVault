"""
MongoDB connection module for MovieVault implementing the Singleton pattern.
Ensures a single shared instance of MongoClient and Database throughout the
application lifecycle, optimizing connection pool usage and system resources.
"""
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database

from config import MONGO_URL, MONGO_DATABASE_NAME
from db.BaseConnection import BaseConnection


class MongoConnection(BaseConnection):
    """
    Thread-safe Singleton class to manage the MongoDB connection.
    Reuses the MongoClient instance and its internal connection pool.
    """

    def __init__(
        self,
        endpoint: str = MONGO_URL,
        database_name: str = MONGO_DATABASE_NAME,
    ) -> None:
        if self.initialized:
            return

        lock = self._locks.get(self.__class__, self._creation_lock)
        with lock:
            if self.initialized:
                return
            try:
                super().__init__(endpoint)
                self._database_name = database_name
                self._client: MongoClient = MongoClient(
                    self.endpoint,
                    serverSelectionTimeoutMS=800,
                    connectTimeoutMS=800,
                    maxPoolSize=50,
                    minPoolSize=10,
                )
                self._database: Database = self._client[self._database_name]
                self._initialized = True
            except Exception:
                self._instances.pop(self.__class__, None)
                self._initialized = False
                raise ConnectionError(f"Failed to connect to MongoDB at {self.endpoint}. Please check that the MongoDB server is running and accessible.")

    @classmethod
    def instance(
        cls,
        endpoint: str = MONGO_URL,
        database_name: str = MONGO_DATABASE_NAME,
    ) -> "MongoConnection":
        """Returns the unique Singleton instance."""
        if cls not in cls._instances:
            cls(endpoint=endpoint, database_name=database_name)
        return cls._instances[cls]

    @property
    def client(self) -> MongoClient:
        """Gets the active MongoClient instance."""
        return self._client

    @property
    def database(self) -> Database:
        """Gets the active Database instance."""
        return self._database

    @property
    def database_name(self) -> str:
        """Gets the configured database name."""
        return self._database_name

    def close(self) -> None:
        """Closes the client connection pool and resets the singleton instance."""
        if hasattr(self, "_client") and self._client:
            try:
                self._client.close()
            except Exception:
                pass
        super().close()
