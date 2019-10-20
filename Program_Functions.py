from shapely.geometry import Point
import geocoder
import pandas as pd
import geopandas

def load_data():
    data = pd.read_csv('Cleaned_Tacos.csv')
    data = geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(data.longitude, data.latitude))

def get_distance_from_current_location(point):
    g = geocoder.ip('me')
    lat, long = g.latlng
    current_location = Point(lat, long)
    return current_location.distance(point)