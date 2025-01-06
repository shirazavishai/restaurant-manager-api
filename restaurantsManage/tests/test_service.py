import unittest
from unittest.mock import patch, MagicMock
import os
# Ensure the environment variable is set before imports
os.environ["DATABASE_URL"] = "test_connection_string"
# Ensure the app module can be found
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.service import search_required_restaurant, find_restaurants, extract_relevant_styles

class TestRestaurantSearch(unittest.TestCase):

    @patch.dict(os.environ, {"DATABASE_URL": "test_connection_string"})
    @patch("app.service.restaurants", [
        {"name": "Israeli Delight", "style": "israeli", "address": "123 Green St", "openHour": "08:00", "closeHour": "22:00", "vegetarian": "yes", "delivers": "yes"},
        {"name": "Carnivore's Haven", "style": "bbq", "address": "456 Grill Ave", "openHour": "12:00", "closeHour": "23:00", "vegetarian": "no", "delivers": "no"},
        {"name": "Pizza Palace", "style": "italian", "address": "789 Dough Rd", "openHour": "11:00", "closeHour": "22:00", "vegetarian": "yes", "delivers": "yes"},
    ])
    @patch("app.restaurant.is_open_now", return_value=True)
    def test_search_required_restaurant(self, mock_is_open_now):
        query = "Find me a israeli restaurant open now"
        import app.service as service  # Import service after patching environment
        result = service.search_required_restaurant(query)
        self.assertIn("Israeli Delight", result)
        self.assertNotIn("Carnivore's Haven", result)


    @patch.dict(os.environ, {"DATABASE_URL": "test_connection_string"})
    @patch("app.service.restaurants", [
        {"name": "Israeli Delight", "style": "israeli", "address": "123 Green St", "openHour": "08:00", "closeHour": "22:00", "vegetarian": "yes", "delivers": "yes"},
    ])
    def test_find_restaurants_time_match(self):
        query_words = ["israeli", "now"]
        query_string = "Find a israeli restaurant open now"
        with patch("app.restaurant.is_open_now", return_value=True):
            import app.service as service  # Import service after patching environment
            results = service.find_restaurants(query_words, query_string)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Israeli Delight")


    @patch.dict(os.environ, {"DATABASE_URL": "test_connection_string"})
    @patch("app.service.restaurants", [
        {"name": "Pizza Palace", "style": "italian", "address": "789 Dough Rd", "openHour": "11:00", "closeHour": "22:00", "vegetarian": "yes", "delivers": "yes"},
    ])
    def test_find_restaurants_no_match(self):
        query_words = ["bbq", "now"]
        query_string = "Find a bbq restaurant open now"
        with patch("app.restaurant.is_open_now", return_value=False):
            import app.service as service  # Import service after patching environment
            results = service.find_restaurants(query_words, query_string)
        self.assertEqual(len(results), 0)


    @patch.dict(os.environ, {"DATABASE_URL": "test_connection_string"})
    @patch("app.service.restaurants", [
        {"name": "Israeli Delight", "style": "israeli", "address": "123 Green St", "openHour": "08:00", "closeHour": "22:00", "vegetarian": "yes", "delivers": "yes"},
        {"name": "Pizza Palace", "style": "italian", "address": "789 Dough Rd", "openHour": "11:00", "closeHour": "22:00", "vegetarian": "yes", "delivers": "yes"},
    ])
    def test_extract_relevant_styles(self):
        query_words = ["israeli"]
        import app.service as service  # Import service after patching environment
        relevant_restaurants = service.extract_relevant_styles(query_words)
        self.assertEqual(len(relevant_restaurants), 1)
        self.assertEqual(relevant_restaurants[0]["name"], "Israeli Delight")


    @patch.dict(os.environ, {"DATABASE_URL": "test_connection_string"})
    @patch("app.db.save_query_history")
    @patch("app.service.restaurants", [
        {"name": "Israeli Delight", "style": "israeli", "address": "123 Green St", "openHour": "08:00", "closeHour": "22:00", "vegetarian": "yes", "delivers": "yes"},
    ])
    def test_search_logs_query_history(self, mock_save_query_history):
        query = "Find a israeli restaurant open now"
        import app.service as service  # Import service after patching environment
        with patch("app.restaurant.is_open_now", return_value=True):
            service.search_required_restaurant(query)
        mock_save_query_history.assert_called_once()


if __name__ == "__main__":
    unittest.main()
