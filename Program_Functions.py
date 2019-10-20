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
    for sentence in review_arr:
        results = sid.polarity_scores(sentence)
        total_sentiment_value += results['compound']
        no_of_sentences += 1

    sentiment = float(total_sentiment_value / no_of_sentences)

    return sentiment


def getAvgReviews(id, headers):
    #url = "https://api.yelp.com/v3/businesses/" + id + "/reviews"
    url = "https://api.yelp.com/v3/businesses/" + id
    req = requests.get(url, headers=headers)

    business = json.loads(req.text)

    # with open('reviews.txt', 'w') as outfile:
    #     json.dump(reviews, outfile, indent=4, sort_keys=True)

    return business['rating']

def getReviewCount(id, headers):
    url = "https://api.yelp.com/v3/businesses/" + id + "/reviews"
    req = requests.get(url, headers=headers)
    reviews = json.loads(req.text)

    return len(reviews['reviews'])    return current_location.distance(point)

def yelp():
    api_key = get_yelp_api_key()
    headers = {'Authorization': 'Bearer %s' % api_key}

    url = 'https://api.yelp.com/v3/businesses/matches'

    params = {'name': 'The Habit Burger Grill',
              'address1': '604 S Mooney Blvd',
              'city': 'Visalia',
              'state': 'CA',
              'zip_code': '93277',
              'country': 'US'}

    req = requests.get(url, params=params, headers=headers)

    json_data = json.loads(req.text)

    with open('query.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4, sort_keys=True)

    id = json_data['businesses'][0]['id']

    print(getAvgReviews(id, headers))
    print(getReviewCount(id, headers))

def getSentiment(review_arr):
    sid = SentimentIntensityAnalyzer()
    total_sentiment_value = 0
    no_of_sentences = 0

    for sentence in review_arr:
        results = sid.polarity_scores(sentence)
        total_sentiment_value += results['compound']
        no_of_sentences += 1

    sentiment = float(total_sentiment_value / no_of_sentences)

    return sentiment


def getAvgReviews(id, headers):
    #url = "https://api.yelp.com/v3/businesses/" + id + "/reviews"
    url = "https://api.yelp.com/v3/businesses/" + id

    req = requests.get(url, headers=headers)

    business = json.loads(req.text)

    # with open('reviews.txt', 'w') as outfile:
    #     json.dump(reviews, outfile, indent=4, sort_keys=True)

    return business['rating']

def getReviewCount(id, headers):
    url = "https://api.yelp.com/v3/businesses/" + id + "/reviews"
    req = requests.get(url, headers=headers)
    reviews = json.loads(req.text)

    return len(reviews['reviews'])