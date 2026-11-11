from pathlib import Path
import dotenv
import os

# Base directory paths
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BACKEND_DIR.parent
ENV_FILE = ROOT_DIR / ".env"

dotenv.load_dotenv(dotenv_path=ENV_FILE)

DEFAULT_MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017/"
DEFAULT_DB_NAME = os.getenv("MONGO_DB_NAME") or "movievault"

TMDB_READ_ACCESS_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN") or ""
TMDB_API_URL = os.getenv("BASE_TMDB_API_URL") or "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = os.getenv("BASE_TMDB_IMAGE_URL") or "https://image.tmdb.org/t/p/w500"

DEFAULT_CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
DEFAULT_CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
DEFAULT_CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "movievault")

DEFAULT_DGRAPH_HOST = os.getenv("DGRAPH_HOST", "localhost")
DEFAULT_DGRAPH_PORT = int(os.getenv("DGRAPH_PORT", "9080"))
DEFAULT_DGRAPH_ALPHA_URL = os.getenv(
    "DGRAPH_ALPHA_URL", f"{DEFAULT_DGRAPH_HOST}:{DEFAULT_DGRAPH_PORT}"
)