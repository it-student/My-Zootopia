"""
This module fetches data from api-ninja's api and returns the json-responsegit
"""
import requests

BASE_URL = "https://api.api-ninjas.com/v1/animals"
KEY = "A3ZgTy43hrThZRH2n1wzvepT7IPhL4N9tW4MEsYD"


def fetch_data(animal_name = ''):
    """ Loads a JSON response from an API """
    if animal_name == '':
        payload = {'name': 'Fox'}
    else:
        payload = {'name': animal_name}
    headers = {'X-Api-Key': KEY}
    response = requests.get(BASE_URL, headers=headers, params=payload)
    return response.json()
