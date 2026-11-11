from pathlib import Path
import dotenv

# Base directory paths
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BACKEND_DIR.parent
ENV_FILE = ROOT_DIR / ".env"

DEFAULT_MONGO_URI = dotenv.get_key(ENV_FILE, "MONGO_URI") or "mongodb://localhost:27017/"
DEFAULT_DB_NAME = dotenv.get_key(ENV_FILE, "MONGO_DB_NAME") or "movievault"
TMDB_API_KEY = dotenv.get_key(ENV_FILE, "TMDB_API_KEY") or ""