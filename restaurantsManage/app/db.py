import pyodbc
from typing import Optional

server = 'your-server-name.database.windows.net'
database = 'your-database-name'
username = 'your-username'
password = 'your-password'
driver = '{ODBC Driver 17 for SQL Server}'

def get_db_connection() -> pyodbc.Connection:
    """Establish a connection to the Azure SQL Database."""
    return pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
