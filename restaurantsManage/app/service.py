import re
import os
import json
import app.restaurant
import pyodbc
from fuzzywuzzy import fuzz
import dateparser
from datetime import datetime
from app.restaurant import Restaurant


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

    if (matching_restaurants[5]):
        recommendation = matching_restaurants[5]
    elif (matching_restaurants[4]):
        recommendation = matching_restaurants[4]
    elif (matching_restaurants[3]):
        recommendation = matching_restaurants[3]
    elif (matching_restaurants[2]):
        recommendation = matching_restaurants[2]
    elif (matching_restaurants[1]):
        recommendation = matching_restaurants[1]
    else: 
        recommendation = "No matching restaurant found"
    
    # Log the query history to the database
    save_query_history(query_string, recommendation)

    recommendation_json = json.dumps(recommendation)
    return recommendation_json


# Search the local restaurant data with fuzzy matching
def find_restaurants(query_words,query_string):
    matching_restaurants = dict=()
    for restaurant in restaurants:
        match_score = 0

        # Check for fuzzy matches on style and address
        for word in query_words:
            if fuzz.partial_ratio(word, restaurant['style'].lower()) > 75:
                match_score += 1
            if fuzz.partial_ratio(word, restaurant['address'].lower()) > 75:
                match_score += 1

        # Check for exact matches on vegetarian and delivery
        if 'vegetarian' in query_words and restaurant['vegetarian'] == 'yes':
            match_score += 1
        if 'delivery' in query_words and restaurant['delivers'] == 'yes':
            match_score += 1

        # Check if the restaurant is open in the required time if given
        if 'now' in query_words:
            if app.restaurant.is_open_now(restaurant['openHour'], restaurant['closeHour']):
                match_score += 1
        else:
            time_words = extract_time_from_query(query_string)
            if not time_words:
                continue
            parsed_time = dateparser.parse(time_words[0][0].lower())
            if parsed_time and app.restaurant.is_open_at_time(parsed_time.strftime('%H:%M'), restaurant['openHour'], restaurant['closeHour']):
                match_score += 1


        if match_score > 0:
            if match_score not in matching_restaurants:
                matching_restaurants[match_score] = []
            matching_restaurants[match_score].append(Restaurant(
                name=restaurant['name'],
                style=restaurant['style'],
                address=restaurant['address'],
                open_hour=restaurant['openHour'],
                close_hour=restaurant['closeHour'], 
                vegetarian=restaurant['vegetarian'], 
                delivery=restaurant['delivers']
            ))

    # Sort the matching restaurants by match score in descending order
 #   sorted_matching_restaurants = dict(sorted(matching_restaurants.items(), key=lambda item: item[0], reverse=True))

    return sorted_matching_restaurants


# Preprocess the user input to remove stopwords and punctuation
def preprocess_query(query):
    stopwords = ['is', 'the', 'a', 'an', 'that', 'and']
    query = query.lower()  # case insensitive
    query = re.sub(r'[^\w\s]', '', query)  # remove punctuation
    words = [word for word in query.split() if word not in stopwords]
    return words


def extract_time_from_query(query):
    # Regex to find time-related words
    time_keywords = [
        r'\b(now|today|tomorrow|in \d+\s*(minutes?|hours?|days?)|at \d{1,2}(:\d{2})?\s*(AM|PM)?)\b',  # match relative time expressions and time like "9 AM"
    ]
    pattern = "|".join(time_keywords)
    matches = re.findall(pattern, query, flags=re.IGNORECASE)
    
    return matches




# SQL query to save query history to the database
def save_query_history(query, recommendation):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    sql_query = """
        INSERT INTO requested_history (query, recommendation, timestamp)
        VALUES (?, ?, ?)
    """

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(sql_query, (query, json.dumps(recommendation), timestamp))

    conn.commit()
    conn.close()

