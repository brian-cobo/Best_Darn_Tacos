# !/usr/bin/env python -W ignore::DeprecationWarning

from shapely.geometry import Point
import geocoder
import pandas as pd
import geopandas
import requests
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import json
import math
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np

from Get_Yelp_API_Key import get_yelp_api_key


"""TODO:
    convert price into $$$$ signs
"""
def load_data():
    data = pd.read_csv('Cleaned_Tacos.csv')
    data = pd.DataFrame(geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(data.longitude, data.latitude)))
    data['score'] = 0
    return data

def get_restaurants_in_same_zipcode(data, zipcode):
    query_results = data[(data.postalCode == zipcode) & (data.geometry != 'POINT (nan nan)')]
    if len(query_results) == 0:
        print('Could not find any listed restaurants in your zipcode')
        exit(0)
    else:
        return query_results

def get_distance_from_current_location(point):
    g = geocoder.ip('me')
    lat, long = g.latlng
    current_location = Point(lat, long)
    return current_location.distance(point)


def yelp(restaurant_name, address, city, state, zipcode):
    data = load_data()
    api_key = get_yelp_api_key()
    headers = {'Authorization': 'Bearer %s' % api_key}

    url = 'https://api.yelp.com/v3/businesses/matches'

    params = {'name': restaurant_name,
              'address1': address,
              'city': city,
              'state': state,
              'zip_code': zipcode,
              'country': 'US'}

    req = requests.get(url, params=params, headers=headers)

    json_data = json.loads(req.text)

    with open('query.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)

    id = json_data['businesses'][0]['id']

    avg_reviews, price = getAvgReviews(id, headers)
    review_count = getReviewCount(id, headers)
    return avg_reviews, review_count, price


def getAvgReviews(id, headers):
    url = "https://api.yelp.com/v3/businesses/" + id
    req = requests.get(url, headers=headers)
    business = json.loads(req.text)
    return business['rating'], business['price']

def getReviewCount(id, headers):
    url = "https://api.yelp.com/v3/businesses/" + id + "/reviews"
    req = requests.get(url, headers=headers)
    reviews = json.loads(req.text)
    return len(reviews['reviews'])

def rate_restaurants(budget,
                     restaurants):
®
    for i in range(len(restaurants)):
        try:
            avg_reviews, review_count, price = yelp(restaurants.name,
                     restaurants.address,
                     restaurants.city,
                     restaurants.province,
                     restaurants.postalCode)
            distance = (0 - get_distance_from_current_location(restaurants.iloc[i].geometry)) * 0.01
            budget = ((budget - restaurants.iloc[i].priceRangeMax) + (budget - restaurants.iloc[i].priceRangeMin)) * 0.3
            if math.isnan(budget):
                budget = -25
            yelp = (avg_reviews * review_count) * 0.1
            score = float(round((distance + budget + yelp), 5))
            restaurants.set_value(i, 'score', score)
        except Exception as e:
            pass
    restaurants = restaurants.sort_values(by='score')
    return restaurants

def print_results_nicely(restaurants):
    reccomendations = []
    for i in range(len(restaurants)):
        reccomendations.append(restaurants.iloc[i].to_dict())
    return reccomendations


def save_user_choice(restaurant):
    restaurant = pd.DataFrame(restaurant).T
    print(restaurant)
    print(restaurant.columns)
    # for column in restaurant.index:
    #     if 'unnamed' in column.lower():
    #         restaurant = restaurant.drop(labels = [column])
    # print(restaurant.index)
    # # for column in restaurant.column:
    # #     if 'unnamed' in column.lower():
    # #         restaurant.drop(column, axis = 1)
    # restaurant.to_csv('User_Picks.csv')

def main(budget, zipcode):
    zipcode = str(zipcode)
    taco_data = load_data()
    restaurants = get_restaurants_in_same_zipcode(taco_data, zipcode)
    rated_restaurants = rate_restaurants(budget, restaurants)
    print_results_nicely(rated_restaurants.iloc[:10])
    save_user_choice(rated_restaurants.iloc[0])


main(30, 77840)
