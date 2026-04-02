import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import sys

sys.dont_write_bytecode = True

# Load .env file
load_dotenv()
# Central JWT Secret (CRITICAL: Must be same for login & verification)
JWT_SECRET = os.getenv("JWT_SECRET", "default_secret_key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 24))

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

class Config:
    SMTP_SERVER = os.getenv("MAIL_SERVER")
    SMTP_PORT = int(os.getenv("MAIL_PORT"))
    SMTP_USERNAME = os.getenv("MAIL_USERNAME")
    SMTP_PASSWORD = os.getenv("MAIL_PASSWORD")

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    conn.autocommit = True

    return conn
