"""
This module fetches data from api-ninja's api and returns the json-responsegit
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.api-ninjas.com/v1/animals"
KEY = os.getenv('API_KEY')


def fetch_data(animal_name = ''):
    """ Loads a JSON response from an API """
    if animal_name == '':
        payload = {'name': 'Fox'}
    else:
        payload = {'name': animal_name}
    headers = {'X-Api-Key': KEY}
    response = requests.get(BASE_URL, headers=headers, params=payload)
    return response.json()
