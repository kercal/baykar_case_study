from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geopy.distance

# nutze OpenStreetMap
geolocator = Nominatim(user_agent="example app")

# insert address as string
def getLocation(address):
    try:
        ort = geolocator.geocode(address)
        if ort:
            return ort.point
        return None
    except GeocoderTimedOut as e:
        return None

# gibt Distanz zwischen zwei Punkten in km aus
def getDistance(location1, location2):
    return geopy.distance.distance(location1, location2).kilometers