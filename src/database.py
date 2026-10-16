"""MySQL connection helpers."""
from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error
from src.config import get_db_config


@contextmanager
def get_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**get_db_config())
        yield connection
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def test_connection():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
        return True, f"Connected to MySQL {version}"
    except (Error, RuntimeError) as exc:
        return False, str(exc)
