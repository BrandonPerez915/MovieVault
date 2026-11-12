"""
Apache Cassandra connection module for MovieVault implementing the Singleton pattern.
Ensures a single shared instance of Cluster and Session throughout the
application lifecycle, managing connection pooling and CQL execution.
"""
from typing import Optional, List
from cassandra.cluster import Cluster, Session

from config import (
    CASSANDRA_HOST,
    CASSANDRA_PORT,
    CASSANDRA_KEYSPACE,
)
from databases.connection import BaseConnection


class CassandraConnection(BaseConnection):
    """
    Thread-safe Singleton class to manage the Apache Cassandra connection.
    Reuses the Cluster instance and its internal Session connection pool.
    """

    def __init__(
        self,
        hosts: Optional[str] = None,
        port: Optional[int] = None,
        keyspace: Optional[str] = None,
        nodes: Optional[List[str]] = None,
    ) -> None:
        if getattr(self, "_initialized", False):
            return

        lock = self._locks.get(self.__class__, self._creation_lock)
        with lock:
            if getattr(self, "_initialized", False):
                return
            try:
                if hosts:
                    endpoint = hosts
                    nodes = nodes or [host.strip() for host in hosts.split(",") if host.strip()]
                elif nodes:
                    endpoint = ",".join(nodes)
                    nodes = nodes
                else:
                    endpoint = CASSANDRA_HOST
                    nodes = [CASSANDRA_HOST]

                super().__init__(endpoint)
                self._nodes: List[str] = nodes
                self._port: int = port or CASSANDRA_PORT
                self._keyspace: str = keyspace or CASSANDRA_KEYSPACE

                self._cluster: Cluster = Cluster(
                    contact_points=self._nodes,
                    port=self._port,
                    connect_timeout=10,
                )
                # Connect session without keyspace first (so keyspace can be created if needed)
                self._session: Session = self._cluster.connect()
                self._initialized = True
            except Exception:
                self._instances.pop(self.__class__, None)
                self._initialized = False
                raise ConnectionError(f"Failed to connect to Cassandra at {self.endpoint}. Please check that the Cassandra server is running and accessible.")

    @classmethod
    def instance(
        cls,
        hosts: Optional[str] = None,
        nodes: Optional[List[str]] = None,
        port: Optional[int] = None,
        keyspace: Optional[str] = None,
    ) -> "CassandraConnection":
        """Returns the unique Singleton instance."""
        if cls not in cls._instances:
            cls(hosts=hosts, port=port, keyspace=keyspace, nodes=nodes)
        return cls._instances[cls]


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

    @property
    def nodes(self) -> List[str]:
        """Gets the contact point nodes list."""
        return self._nodes

    @property
    def port(self) -> int:
        """Gets the connection port."""
        return self._port

    def set_keyspace(self, keyspace: str) -> None:
        """Switches the active session keyspace."""
        self._keyspace = keyspace
        self._session.set_keyspace(keyspace)

    def close(self) -> None:
        """Closes the session and cluster connections and resets the singleton."""
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
        super().close()
