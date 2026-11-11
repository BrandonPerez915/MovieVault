"""
Apache Cassandra connection module for MovieVault implementing the Singleton pattern.
Ensures a single shared instance of Cluster and Session throughout the
application lifecycle, managing connection pooling and CQL execution.
"""
import threading
from typing import Optional, Any, List
from cassandra.cluster import Cluster, Session

from config import (
    DEFAULT_CASSANDRA_HOST,
    DEFAULT_CASSANDRA_PORT,
    DEFAULT_CASSANDRA_KEYSPACE,
)


class CassandraConnection:
    """
    Thread-safe Singleton class to manage the Apache Cassandra connection.
    Reuses the Cluster instance and its internal Session connection pool.
    """

    _instance: Optional["CassandraConnection"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(
        cls,
        nodes: Optional[List[str]] = None,
        port: Optional[int] = None,
        keyspace: Optional[str] = None,
    ) -> "CassandraConnection":
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
        nodes: Optional[List[str]] = None,
        port: Optional[int] = None,
        keyspace: Optional[str] = None,
    ) -> None:
        if getattr(self, "_initialized", False):
            return

        with self._lock:
            if getattr(self, "_initialized", False):
                return
            self._nodes = nodes or 1
            self._port = port or DEFAULT_CASSANDRA_PORT
            self._keyspace = keyspace or DEFAULT_CASSANDRA_KEYSPACE

            self._cluster: Cluster = Cluster(
                contact_points=self._nodes,
                port=self._port,
                connect_timeout=10,
            )
            # Connect session without keyspace first (so keyspace can be created if needed)
            self._session: Session = self._cluster.connect()
            self._initialized = True

    @classmethod
    def instance(
        cls,
        nodes: Optional[List[str]] = None,
        port: Optional[int] = None,
        keyspace: Optional[str] = None,
    ) -> "CassandraConnection":
        """Returns the unique Singleton instance."""
        if cls._instance is None:
            cls(nodes, port, keyspace)
        return cls._instance

    @classmethod
    def get_instance(
        cls,
        nodes: Optional[List[str]] = None,
        port: Optional[int] = None,
        keyspace: Optional[str] = None,
    ) -> "CassandraConnection":
        """Alias for instance() for unified access."""
        return cls.instance(nodes, port, keyspace)

    @property
    def cluster(self) -> Cluster:
        """Gets the active Cluster instance."""
        return self._cluster

    @property
    def session(self) -> Session:
        """Gets the active CQL Session instance."""
        return self._session

    @property
    def keyspace(self) -> str:
        """Gets the target keyspace name."""
        return self._keyspace

    def set_keyspace(self, keyspace: str) -> None:
        """Switches the active session keyspace."""
        self._keyspace = keyspace
        self._session.set_keyspace(keyspace)

    def close(self) -> None:
        """Closes the session and cluster connections and resets the singleton."""
        with self._lock:
            if hasattr(self, "_session") and self._session:
                try:
                    self._session.shutdown()
                except Exception:
                    pass
            if hasattr(self, "_cluster") and self._cluster:
                try:
                    self._cluster.shutdown()
                except Exception:
                    pass
            CassandraConnection._instance = None
            self._initialized = False