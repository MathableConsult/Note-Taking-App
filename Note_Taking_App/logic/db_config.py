import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"