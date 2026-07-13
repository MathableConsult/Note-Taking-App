# Previous implementation for Mysql

# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Add a .env.example file to indicate that users should
# # create a .env file with their own database credentials.

# # Configuration dictionary for connecting to the MySQL database.
# # It will load the parameters from the .env file
# # Best practise for security and flexibility, 
# # especially when deploying to different environments.
# db_config = {
#     "host": os.getenv("DB_HOST"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "database": os.getenv("DB_NAME")
# }

# # I assume you have a /uploads directory in your project
# # Include the instruction to create it if it doesn't exist
# UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/")
# DEBUG = os.getenv("DEBUG", "False").lower() == "true"

import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env variables
load_dotenv()

# --- DATABASE CONFIGURATION ---
# Check if the hidden deployment secrets folder exists locally in your project
local_secrets_exist = os.path.exists(os.path.join(os.getcwd(), ".streamlit", "secrets.toml"))

# Only access st.secrets if we are running on Streamlit Cloud OR a local secrets file exists
if "STREAMLIT_SERVER_PORT" not in os.environ or local_secrets_exist:
    # Production Remote / Explicit Local Secret Mode
    # DB_PATH = st.secrets.get("DB_PATH", "remote_database.db")
    DB_PATH = os.getenv("DB_PATH", "local_database.db")
else:
    # Local Development Mode: Safely pull from your .env file without touching st.secrets
    DB_PATH = os.getenv("DB_PATH", "local_database.db")

db_config = {
    "database": DB_PATH
}

# --- DIRECTORY CONFIGURATION ---
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads/")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

if not os.path.exists(UPLOAD_DIR):
    try:
        os.makedirs(UPLOAD_DIR)
    except OSError:
        pass
