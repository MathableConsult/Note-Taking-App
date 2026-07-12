import os
from dotenv import load_dotenv

load_dotenv()

# Add a .env.example file to indicate that users should
# create a .env file with their own database credentials.

# Configuration dictionary for connecting to the MySQL database.
# It will load the parameters from the .env file
# Best practise for security and flexibility, 
# especially when deploying to different environments.
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# I assume you have a /uploads directory in your project
# Include the instruction to create it if it doesn't exist
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"