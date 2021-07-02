from flask.globals import request
from flask.wrappers import Response
import requests, json

response = requests.get('https://www.themealdb.com/api/json/v1/1/filter.php?i=chicken_breast')


print (response.json())


# def get_meal_list(search_input):
#     url=f'https://www.themealdb.com/api/json/v1/1/filter.php?i=${ search_input }'
#     response= requests.get(url).json()
#     return response


