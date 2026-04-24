import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Create a MySQL connection using environment variables.

    Copy `.env.example` to `.env` and update the values for your local setup.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "turnero_estetica"),
        port=int(os.getenv("DB_PORT", "3306")),
    )
