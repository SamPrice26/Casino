# config.py
import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from the .env file
load_dotenv()

# Fetch values from environment variables, or set default values
DATABASE_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_USER = os.getenv("DB_USER", "root")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")  # Don't use a default value for the password
DATABASE_NAME = os.getenv("DB_NAME", "casino_db")

# Function to create DB connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,  # Password fetched from the .env file
        database=DATABASE_NAME
    )
    return connection