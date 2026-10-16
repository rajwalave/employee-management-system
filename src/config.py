"""Load database configuration from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_config():
    required = ("DB_HOST", "DB_USER", "DB_NAME")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(
            "Missing configuration: " + ", ".join(missing)
            + ". Copy .env.example to .env and fill in your MySQL settings."
        )
    try:
        port = int(os.getenv("DB_PORT", "3306"))
    except ValueError as exc:
        raise RuntimeError("DB_PORT must be an integer.") from exc
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": port,
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "employee_management"),
        "connection_timeout": 8,
    }
