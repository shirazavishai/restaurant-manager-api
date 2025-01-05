import os
import pyodbc
import json
from datetime import datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables from .env file if running locally
if os.getenv('ENVIRONMENT') == 'local':
    load_dotenv()

connection_string = os.getenv('DATABASE_URL')

if connection_string is None:
    raise ValueError("DATABASE_URL environment variable is not set.")

encryption_key = Fernet.generate_key()  # Save this securely
cipher = Fernet(encryption_key)

def encrypt_data(data: str) -> str:
    """Encrypt data using Fernet symmetric encryption."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    """Decrypt data using Fernet symmetric encryption."""
    return cipher.decrypt(data.encode()).decode()


def save_query_history(query, recommendation):
    """Save the query history to the database."""
    try:
        # Establish a database connection using the connection string
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Encrypt sensitive fields
        encrypted_query = encrypt_data(query)
        encrypted_recommendation = encrypt_data(json.dumps(recommendation))

        # SQL query to save query history
        sql_query = """
            INSERT INTO requested_history (request_query, recommendation_response, timestamp)
            VALUES (?, ?, ?)
        """

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Execute the SQL query with query, recommendation (as JSON), and timestamp
        cursor.execute(sql_query, (encrypted_query, json.dumps(encrypted_recommendation), timestamp))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving query history: {e}")
        # raise
    finally:
        if 'conn' in locals():
            conn.close()


# Not in use...
def get_query_history():
    try:

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        sql_query = "SELECT request_query, recommendation_response, timestamp FROM requested_history"
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        return [
            {
                "request_query": decrypt_data(row.request_query),
                "recommendation_response": decrypt_data(row.recommendation_response),
                "timestamp": row.timestamp,
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error getting query history: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()
    