"""
Dgraph connection module for MovieVault implementing the Singleton pattern.
Ensures a single shared instance of DgraphClient and DgraphClientStub via gRPC throughout the
application lifecycle, managing graph traversals, mutations, and query execution.
"""
import threading
from typing import Optional, Any
import pydgraph

from config import DEFAULT_DGRAPH_ALPHA_URL


class DgraphConnection:
    """
    Thread-safe Singleton class to manage the Dgraph connection.
    Reuses the DgraphClient and gRPC Stub connection pool.
    """

    _instance: Optional["DgraphConnection"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(
        cls,
        endpoint: Optional[str] = None,
    ) -> "DgraphConnection":
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
        endpoint: Optional[str] = None,
    ) -> None:
        if getattr(self, "_initialized", False):
            return

        with self._lock:
            if getattr(self, "_initialized", False):
                return
            self._endpoint = endpoint or DEFAULT_DGRAPH_ALPHA_URL
            self._stub = pydgraph.DgraphClientStub(self._endpoint)
            self._client = pydgraph.DgraphClient(self._stub)
            self._initialized = True

    @classmethod
    def instance(
        cls,
        endpoint: Optional[str] = None,
    ) -> "DgraphConnection":
        """Returns the unique Singleton instance."""
        if cls._instance is None:
            cls(endpoint)
        return cls._instance

    @classmethod
    def get_instance(
        cls,
        endpoint: Optional[str] = None,
    ) -> "DgraphConnection":
        """Alias for instance() for unified access."""
        return cls.instance(endpoint)

    @property
    def client(self) -> Any:
        """Gets the active DgraphClient instance."""
        return self._client

    @property
    def stub(self) -> Any:
        """Gets the active gRPC DgraphClientStub instance."""
        return self._stub

    @property
    def endpoint(self) -> str:
        """Gets the gRPC Alpha endpoint address."""
        return self._endpoint

    def close(self) -> None:
        """Closes gRPC channel and resets the singleton."""
        with self._lock:
            if hasattr(self, "_stub") and self._stub:
                try:
                    self._stub.close()
                except Exception:
                    pass
            DgraphConnection._instance = None
            self._initialized = False
