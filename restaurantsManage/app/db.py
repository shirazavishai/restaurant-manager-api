import os
import pyodbc
import json
from datetime import datetime

# Retrieve the database connection string from the environment variable (injected by terraform)
connection_string = "test"
#connection_string = os.getenv('DATABASE_URL')
if connection_string is None:
    raise ValueError("DATABASE_URL environment variable is not set.")

def save_query_history(query, recommendation):
    """Save the query history to the database."""
    # Establish a database connection using the connection string
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # SQL query to save query history
    sql_query = """
        INSERT INTO requested_history (query, recommendation, timestamp)
        VALUES (?, ?, ?)
    """

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Execute the SQL query with query, recommendation (as JSON), and timestamp
    cursor.execute(sql_query, (query, json.dumps(recommendation), timestamp))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
