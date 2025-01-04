import re
import os
import json
import app.restaurant
import app.db
from fuzzywuzzy import fuzz
import dateparser
from datetime import datetime

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/data"
json_file_path = os.path.join(base_dir, 'restaurants.json')
with open(json_file_path, 'r') as f:
    restaurants = json.load(f)



def search_required_restaurant(query_string: str):
    """
    Search for a restaurant based on the required parameters
    """
    query_words = preprocess_query(query_string)
    matching_restaurants = find_restaurants(query_words,query_string)

    if not matching_restaurants:
        print("No matching restaurants found")
        return "No matching restaurants found"

    # Log the query history to the database
    app.db.save_query_history(query_string, matching_restaurants)

    json_string = ""
    for restaurant in matching_restaurants:
        json_string+=restaurant.to_json_string()

    return json_string



def find_restaurants(query_words, query_string):
    relevant_restaurants = extract_relevant_styles(query_words)
    if not relevant_restaurants:
        return []  # No matching styles, so no results

    matching_restaurants = []
    current_time = datetime.now().strftime('%H:%M')  # Current time for "now"

    vegetarian_keywords = ["vegetarian", "vegan", "veg", "vegie","veggy","veggie","veggies","vegg","veget"]

    for restaurant in relevant_restaurants:

        restaurant_vegetarian = str(restaurant['vegetarian']).lower()
        restaurant_open_hour = restaurant['openHour']
        restaurant_close_hour = restaurant['closeHour']

        # 1. Time Matching
        time_matched = False
        if 'now' in query_words:
            time_matched = app.restaurant.is_open_now(
                restaurant_open_hour, restaurant_close_hour
            )
        else:
            time_words = extract_time_from_query(query_string)
            if time_words:
                parsed_time = dateparser.parse(time_words[0].lower())
                if parsed_time:
                    time_matched = app.restaurant.is_open_at_time(
                        parsed_time.strftime('%H:%M'),
                        restaurant_open_hour,
                        restaurant_close_hour
                    )
            else:
                time_matched = True

        if not time_matched:
            continue

        require_vegetarian = False
        for keyword in vegetarian_keywords:
            if keyword in query_words:
                require_vegetarian = True
        if (require_vegetarian and restaurant_vegetarian != "yes"):
            continue

        # If all criteria match, add the restaurant to results
        matching_restaurants.append(app.restaurant.Restaurant(
            name=restaurant['name'],
            style=restaurant['style'],
            address=restaurant['address'],
            open_hour=restaurant_open_hour,
            close_hour=restaurant_close_hour,
            vegetarian=restaurant['vegetarian'],
            delivery=restaurant['delivers']
        ))

    return matching_restaurants


def extract_relevant_styles(query_words):
    """
    Extract styles from the query and match them with the available restaurant styles.
    """
    all_styles = {restaurant['style'].lower() for restaurant in restaurants}
    the_style = ""

    for word in query_words:
        for style in all_styles:
            if fuzz.partial_ratio(word, style) > 75:
                the_style = style
    
    relevant_restaurants = []
    for restaurant in restaurants:
        if restaurant['style'].lower() == the_style:
            relevant_restaurants.append(restaurant)

    return relevant_restaurants


# Preprocess the user input to remove stopwords and punctuation
def preprocess_query(query):
    stopwords = ['is', 'the', 'a', 'an', 'that', 'and']
    query = query.lower()  # case insensitive
    query = re.sub(r'[^\w\s:]', '', query)  # remove punctuation
    words = [word for word in query.split() if word not in stopwords]
    return words


def extract_time_from_query(query):
    # Regex to find time-related words, ensuring full hour format (HH:MM)
    time_keywords = [
        r'\b(now|today|tomorrow|in \d+\s*(minutes?|hours?|days?)|at \d{1,2}(:[0-5]\d)\s*(AM|PM)?)\b',  # match relative time expressions and time like "9 AM", "12:30 PM"
    ]
    pattern = "|".join(time_keywords)
    matches = re.findall(pattern, query, flags=re.IGNORECASE)
    
    # Extract the full match from the tuples returned by re.findall
    filtered_matches = [match[0] for match in matches if match[0]]
    
    return filtered_matches
