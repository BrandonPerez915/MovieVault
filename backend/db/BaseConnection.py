"""
Abstract Base Connection module for MovieVault database connections.
Implements the Singleton pattern with thread-safe double-checked locking per subclass,
endpoint management, and standardized lifecycle hooks.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Self
import threading


class BaseConnection(ABC):
    """
    Abstract base class providing thread-safe Singleton management
    and unified lifecycle behavior for all database connections.
    """

    # Each subclass will have its own instance and reentrant lock
    _instances: Dict[type, Any] = {}
    _locks: Dict[type, threading.RLock] = {}

    # Global lock to ensure thread-safe creation of subclass locks
    _creation_lock: threading.Lock = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls is BaseConnection:
            raise TypeError("BaseConnection is an abstract base class and cannot be instantiated directly.")

        # Ensure that a reentrant lock exists for this subclass
        if cls not in cls._locks:
            with cls._creation_lock:
                if cls not in cls._locks:
                    cls._locks[cls] = threading.RLock()

        # Double-checked locking pattern for thread safety
        if cls not in cls._instances:
            with cls._locks[cls]:
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instances[cls] = instance

        return cls._instances[cls]

    def __init__(self, endpoint: str) -> None:
        if getattr(self, "_initialized", False):
            return

        if endpoint is None or not str(endpoint).strip():
            raise ValueError("Endpoint is required for the initialization of the Singleton.")

        self._endpoint = str(endpoint).strip()

    @property
    def endpoint(self) -> str:
        """Returns the endpoint of the connection. Raises an AttributeError if not initialized."""
        if not hasattr(self, "_endpoint"):
            raise AttributeError("Connection instance has not been initialized with an endpoint.")
        return self._endpoint

    @property
    def initialized(self) -> bool:
        """Returns True if the connection instance has finished initialization."""
        return getattr(self, "_initialized", False)

    @classmethod
    @abstractmethod
    def instance(cls: type[Self], *args: Any, **kwargs: Any) -> Self:
        """Returns the unique Singleton instance."""
        if cls not in cls._instances:
            cls(*args, **kwargs)
        return cls._instances[cls]


    @abstractmethod
    def close(self) -> None:
        """Closes connection resources and resets the singleton instance."""
        cls = self.__class__
        lock = self._locks.get(cls, self._creation_lock)
        with lock:
            self._instances.pop(cls, None)
            self._initialized = False

    @classmethod
    def reset_instance(cls) -> None:
        """Closes and resets the singleton instance for this connection class."""
        if cls in cls._instances:
            instance = cls._instances[cls]
            instance.close()
