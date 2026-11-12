"""
Dgraph connection module for MovieVault implementing the Singleton pattern.
Ensures a single shared instance of DgraphClient and DgraphClientStub via gRPC throughout the
application lifecycle, managing graph traversals, mutations, and query execution.
"""
import pydgraph

from config import DGRAPH_URL
from db.BaseConnection import BaseConnection


class DgraphConnection(BaseConnection):
    """
    Thread-safe Singleton class to manage the Dgraph connection.
    Reuses the DgraphClient and gRPC Stub connection pool.
    """

    def __init__(
        self,
        endpoint: str = DGRAPH_URL,
    ) -> None:
        if getattr(self, "_initialized", False):
            return

        lock = self._locks.get(self.__class__, self._creation_lock)
        with lock:
            if getattr(self, "_initialized", False):
                return
            try:
                super().__init__(endpoint)
                self._stub: pydgraph.DgraphClientStub = pydgraph.DgraphClientStub(self.endpoint)
                self._client: pydgraph.DgraphClient = pydgraph.DgraphClient(self._stub)
                self._initialized = True
            except Exception:
                self._instances.pop(self.__class__, None)
                self._initialized = False
                raise ConnectionError(f"Failed to connect to Dgraph at {self.endpoint}. Please check that the Dgraph server is running and accessible.")


    @classmethod
    def instance(
        cls,
        endpoint: str = DGRAPH_URL,
    ) -> "DgraphConnection":
        """Returns the unique Singleton instance."""
        if cls not in cls._instances:
            cls(endpoint=endpoint)
        return cls._instances[cls]


    @property
    def client(self) -> pydgraph.DgraphClient:
        """Gets the active DgraphClient instance."""
        return self._client


    @property
    def stub(self) -> pydgraph.DgraphClientStub:
        """Gets the active gRPC DgraphClientStub instance."""
        return self._stub


    def close(self) -> None:
        """Closes gRPC channel and resets the singleton."""
        if hasattr(self, "_stub") and self._stub:
            try:
                self._stub.close()
            except Exception:
                pass
        super().close()
