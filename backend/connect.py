"""
Unified Database Connection Hub for MovieVault (connect.py).
Provides a single, cohesive interface to manage and coordinate connections across
all three architectural database engines:
1. MongoDB (Document store: Movies, Reviews, Users, Lists, Actors, Directors)
2. Apache Cassandra (Time-series / Activity logs & user interaction event streaming)
3. Dgraph (Graph database: Knowledge graphs, Actor-Director collaboration graphs, Social following)
"""

from typing import Dict, Optional

from config import (
    MONGO_URL,
    MONGO_DATABASE_NAME,

    CASSANDRA_HOST,
    CASSANDRA_PORT,
    CASSANDRA_KEYSPACE,

    DGRAPH_HOST,
    DGRAPH_PORT,
)
from databases import (
    CassandraConnection,
    MongoConnection,
    DgraphConnection
)


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

        self._mongo_client = None
        self._mongo_database = None
        self._mongo_status = "NOT_INITIALIZED"

        self._cassandra_session = None
        self._cassandra_status = "NOT_INITIALIZED"

        self._dgraph_client = None
        self._dgraph_status = "NOT_INITIALIZED"

        # Initialize connections. Its necessary to call instance with parameters once to configure each database.
        self._mongo_connection = MongoConnection().instance(
            MONGO_URL,
            MONGO_DATABASE_NAME
        )
        self._cassandra_connection = CassandraConnection().instance(
            CASSANDRA_HOST,
            CASSANDRA_PORT,
            CASSANDRA_KEYSPACE
        )
        self._dgraph_connection = DgraphConnection().instance(
            f"{DGRAPH_HOST}:{DGRAPH_PORT}"
        )

        # MongoDB
        try:
            self._mongo_client = self._mongo_connection.client
            self._mongo_database = self._mongo_connection.database
            if self._mongo_connection.initialized:
                self._mongo_status = "INITIALIZED"
            else:
                self._mongo_status = "STANDBY (Not initialized)"
        except Exception as e:
            self._mongo_status = f"STANDBY ({type(e).__name__})"

        # Cassandra
        try:
            self._cassandra_session = self._cassandra_connection.session
            self._cassandra_keyspace = self._cassandra_connection.keyspace
            self._cassandra_cluster = self._cassandra_connection.cluster
            if self._cassandra_connection.initialized:
                self._cassandra_status = "INITIALIZED"
            else:
                self._cassandra_status = "STANDBY (Not initialized)"
        except Exception as e:
            self._cassandra_status = f"STANDBY ({type(e).__name__})"

        # Dgraph
        try:
            self._dgraph_client = self._dgraph_connection.client
            self._dgraph_stub = self._dgraph_connection.stub
            if self._dgraph_connection.initialized:
                self._dgraph_status = "INITIALIZED"
            else:
                self._dgraph_status = "STANDBY (Not initialized)"
        except Exception as e:
            self._dgraph_status = f"STANDBY ({type(e).__name__})"

        self._initialized = True


    @classmethod
    def get_instance(cls) -> "UnifiedDatabaseConnection":
        if cls._instance is None:
            cls()
        return cls._instance


    @property
    def mongodb(self) -> MongoConnection:
        """Returns the active MongoDB database instance."""
        return self._mongo_database


    @property
    def cassandra(self) -> CassandraConnection:
        """Returns the active Cassandra session."""
        return self._cassandra_session


    @property
    def dgraph(self) -> DgraphConnection:
        """Returns the active Dgraph client."""
        return self._dgraph_client


    @property
    def status(self) -> Dict[str, str]:
        """Returns the health status of all connected database engines."""
        return {
            "mongodb": self._mongo_status,
            "cassandra": self._cassandra_status,
            "dgraph": self._dgraph_status,
        }


    def close(self) -> None:
        """Closes all open database connections."""
        self._mongo_connection.close()
        self._mongo_connection = None
        self._mongo_client = None
        self._mongo_database = None
        self._mongo_status = "CLOSED"

        self._cassandra_connection.close()
        self._cassandra_connection = None
        self._cassandra_session = None
        self._cassandra_keyspace = None
        self._cassandra_cluster = None
        self._cassandra_status = "CLOSED"

        self._dgraph_connection.close()
        self._dgraph_connection = None
        self._dgraph_client = None
        self._dgraph_stub = None
        self._dgraph_status = "CLOSED"
