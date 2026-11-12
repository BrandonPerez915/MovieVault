from pathlib import Path
import os
import dotenv

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent
ENV_FILE = ROOT_DIR / ".env"

dotenv.load_dotenv(dotenv_path=ENV_FILE)

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "movievault")

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_DATABASE_NAME = os.getenv("MONGO_DB_NAME", "movievault")
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

DGRAPH_HOST = os.getenv("DGRAPH_HOST", "localhost")
DGRAPH_PORT = int(os.getenv("DGRAPH_PORT", "9080"))
DGRAPH_URL = f"{DGRAPH_HOST}:{DGRAPH_PORT}"

TMDB_READ_ACCESS_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN") or ""
TMDB_API_URL = os.getenv("BASE_TMDB_API_URL") or "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = os.getenv("BASE_TMDB_IMAGE_URL") or "https://image.tmdb.org/t/p/w500"

