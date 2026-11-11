"""
MongoDB connection module for MovieVault implementing the Singleton pattern.
Ensures a single shared instance of MongoClient and Database throughout the
application lifecycle, optimizing connection pool usage and system resources.
"""

from typing import Optional

import dotenv
import threading
from pymongo import MongoClient
from pymongo.database import Database

from config import DEFAULT_MONGO_URI, DEFAULT_DB_NAME


class MongoDBConnection:
    """
    Thread-safe Singleton class to manage the MongoDB connection.
    Reuses the MongoClient instance and its internal connection pool.
    """

    _instance: Optional["MongoDBConnection"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(
        cls,
        uri: str = DEFAULT_MONGO_URI,
        db_name: str = DEFAULT_DB_NAME,
    ) -> "MongoDBConnection":
        # Double-checked locking pattern for thread safety
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instance = instance
        return cls._instance

    def __init__(
        self,
        uri: str = DEFAULT_MONGO_URI,
        db_name: str = DEFAULT_DB_NAME,
    ) -> None:
        if getattr(self, "_initialized", False):
            return

        with self._lock:
            if getattr(self, "_initialized", False):
                return
            self._uri = uri
            self._db_name = db_name
            self._client: MongoClient = MongoClient(
                self._uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=10,
            )
            self._db: Database = self._client[self._db_name]
            self._initialized = True

    @classmethod
    def instance(
        cls,
        uri: str = DEFAULT_MONGO_URI,
        db_name: str = DEFAULT_DB_NAME,
    ) -> "MongoDBConnection":
        """Returns the unique Singleton instance."""
        if cls._instance is None:
            cls(uri, db_name)
        return cls._instance

    @property
    def client(self) -> MongoClient:
        """Gets the active MongoClient instance."""
        return self._client

    @property
    def database(self) -> Database:
        """Gets the active Database instance."""
        return self._db

    def close(self) -> None:
        """Closes the client connection pool and resets the singleton instance."""
        with self._lock:
            if hasattr(self, "_client") and self._client:
                self._client.close()
            MongoDBConnection._instance = None
            self._initialized = False
