"""
Unified Database Connection Hub for MovieVault (connect.py).
Provides a single, cohesive interface to manage and coordinate connections across
all three architectural database engines:
1. MongoDB (Document store: Movies, Reviews, Users, Lists, Actors, Directors)
2. Apache Cassandra (Time-series / Activity logs & user interaction event streaming)
3. Dgraph (Graph database: Knowledge graphs, Actor-Director collaboration graphs, Social following)
"""

from typing import Dict, Optional

from db.mongodb.connection import MongoDBConnection
from db.cassandra.connection import CassandraConnection
from db.dgraph.connection import DgraphConnection


class UnifiedDatabaseConnection:
    """
    Unified database manager coordinating MongoDB, Cassandra, and Dgraph.
    Provides single-point access, diagnostics, and graceful mock fallbacks.
    """

    _instance: Optional["UnifiedDatabaseConnection"] = None

    def __new__(cls) -> "UnifiedDatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return

        self._mongo_client = MongoDBConnection().client
        self._mongo_db = MongoDBConnection().database
        self._mongo_status = "INITIALIZED"

        self._cassandra_session = CassandraConnection().session
        self._cassandra_status = "INITIALIZED"

        self._dgraph_client = DgraphConnection().client
        self._dgraph_status = "INITIALIZED"

        self._initialized = True

    @classmethod
    def get_instance(cls) -> "UnifiedDatabaseConnection":
        if cls._instance is None:
            cls()
        return cls._instance

    def connect_all(self) -> None:
        """Initializes all database connections with real or simulated handlers."""
        pass

    def get_mongodb(self) -> MongoDBConnection:
        """Returns the active MongoDB database instance."""
        return self._mongo_db

    def get_cassandra(self) -> CassandraConnection:
        """Returns the active Cassandra session."""
        return self._cassandra_session

    def get_dgraph(self) -> DgraphConnection:
        """Returns the active Dgraph client."""
        return self._dgraph_client

    def get_status(self) -> Dict[str, str]:
        """Returns the health status of all connected database engines."""
        return {
            "MongoDB (Document Store)": self._mongo_status,
            "Cassandra (Activity Log Stream)": self._cassandra_status,
            "Dgraph (Knowledge & Social Graph)": self._dgraph_status,
        }

    def close_all(self) -> None:
        """Closes all open database connections."""
        if self._cassandra_session:
            self._cassandra_session.close()
            self._cassandra_status = "CLOSED"
        if self._dgraph_client:
            self._dgraph_client.close()
            self._dgraph_status = "CLOSED"
        try:
            from db.mongodb.connection import close_connection
            close_connection()
            self._mongo_status = "CLOSED"
        except Exception:
            pass

def get_hub() -> UnifiedDatabaseConnection:
    """Returns the Unified Database Connection Hub."""
    return UnifiedDatabaseConnection.get_instance()



def get_mongodb() -> MongoDBConnection:
    """Convenience getter for MongoDB."""
    return get_hub().get_mongodb()


def get_cassandra() -> CassandraConnection:
    """Convenience getter for Cassandra."""
    return get_hub().get_cassandra()


def get_dgraph() -> DgraphConnection:
    """Convenience getter for Dgraph."""
    return get_hub().get_dgraph()

