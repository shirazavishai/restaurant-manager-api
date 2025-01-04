import os
import pyodbc
from typing import Optional

# Retrieve the database connection string from the environment variable (injected by terraform)
connection_string = os.getenv('DATABASE_URL')

def get_db_connection() -> pyodbc.Connection:
    """Establish a connection to the Azure SQL Database using the connection string from app settings."""
    if connection_string is None:
        raise ValueError("DATABASE_URL environment variable is not set.")
    
    # Establish the database connection using the connection string
    return pyodbc.connect(connection_string)
