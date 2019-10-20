from shapely.geometry import Point
import geocoder
import pandas as pd
import geopandas
import requests
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from Get_Yelp_API_Key import get_yelp_api_key

def load_data():
    data = pd.read_csv('Cleaned_Tacos.csv')
    data = geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(data.longitude, data.latitude))
    return data

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

    avg_reviews = getAvgReviews(id, headers)
    review_count = getReviewCount(id, headers)
    return avg_reviews, review_count


def getAvgReviews(id, headers):
    url = "https://api.yelp.com/v3/businesses/" + id
    req = requests.get(url, headers=headers)
    business = json.loads(req.text)
    return business['rating']

def getReviewCount(id, headers):
    url = "https://api.yelp.com/v3/businesses/" + id + "/reviews"
    req = requests.get(url, headers=headers)
    reviews = json.loads(req.text)
    return len(reviews['reviews'])
