import unittest
from unittest.mock import patch, MagicMock
import os
import json

class TestDBOperations(unittest.TestCase):

    @patch.dict(os.environ, {"DATABASE_URL": "test_connection_string"})
    @patch("app.db.pyodbc.connect")
    def test_save_query_history(self, mock_connect):
        """Test save_query_history function"""

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock data
        sample_query = "Find vegan restaurants"
        sample_recommendation = [{"name": "Vegan Delight", "address": "123 Green St"}]
        timestamp = "2023-01-01 12:00:00"
        encrypted_query = "encrypted_query_data"
        encrypted_recommendation = "encrypted_recommendation_data"
        
        # Encrypt the values before passing them to the mock
        from app.db import encrypt_data  # Import after patching env
        encrypted_query = encrypt_data(sample_query)
        encrypted_recommendation = encrypt_data(json.dumps(sample_recommendation))

        # Import service module after patching the environment
        import app.service  # This imports the service.py module after environment setup
        
        # Call the function
        from app.db import save_query_history
        save_query_history(sample_query, sample_recommendation)

        # Ensure the cursor executed the correct SQL query
        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO requested_history (request_query, recommendation_response, timestamp)
            VALUES (?, ?, ?)
            """,
            (encrypted_query, json.dumps(encrypted_recommendation), timestamp)
        )

        # Ensure commit and close are called
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch.dict(os.environ, {"DATABASE_URL": "test_connection_string"})
    def test_database_url_set(self):
        """Test that the DATABASE_URL environment variable is set correctly"""
        self.assertEqual(os.getenv('DATABASE_URL'), "test_connection_string")

    @patch.dict(os.environ, {"DATABASE_URL": "test_connection_string"})
    @patch("app.db.pyodbc.connect")
    def test_get_query_history(self, mock_connect):
        """Test get_query_history function"""
        
        # Mock the environment variable and database response
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Prepare mock database return data
        mock_cursor.fetchall.return_value = [
            MagicMock(request_query="encrypted_query", recommendation_response="encrypted_recommendation", timestamp="2023-01-01 12:00:00")
        ]

        # Call the function
        from app.db import get_query_history
        result = get_query_history()

        # Expected result
        expected_result = [
            {
                "request_query": "sample_query",  # Assume decryption works and returns correct value
                "recommendation_response": [{"name": "Vegan Delight", "address": "123 Green St"}],
                "timestamp": "2023-01-01 12:00:00"
            }
        ]
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
