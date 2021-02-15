from flask import Flask, request, abort
from markupsafe import escape
import json
import urllib.request
import urllib.parse
import os
from flask_cors import CORS

# Get OpenWeatherMap APP key from environment file
openweathermap_app_key = os.environ.get("OPEN_WEATHERMAP_APP_KEY")
# Get IPStack access key from environment file
ipstack_access_key = os.environ.get("IPSTACK_ACCESS_KEY")
# Use default lat/lon when failed to get the location from IP
default_lat = os.environ.get("DEFAULT_LAT")
default_lon = os.environ.get("DEFAULT_LON")

app = Flask(__name__)
CORS(app)

print('app started.')

cities = {}
# city.list.json from http://bulk.openweathermap.org/sample/city.list.json.gz
with open('city.list.json') as city_list_file:
    city_data = json.load(city_list_file)
    for one in city_data:
        cities[one['name'].lower()] = {
            "name": one['name'],
            "label": one['name'],
            "id": one['id'],
            "lat": one['coord']['lat'],
            "lon": one['coord']['lon']
        }


@app.route('/', methods=['GET'])
def index():
    ip = request.remote_addr
    print(ip)
    url_str = 'http://api.ipstack.com/{ip}?access_key={ipstack_access_key}'.format(
        ip=ip, ipstack_access_key=ipstack_access_key)
    with urllib.request.urlopen(url_str) as url:
        result = json.loads(url.read().decode())
    print(result)

    myLat = result['latitude']
    myLon = result['longitude']
    if (result['latitude'] is None or result['longitude'] is None):
        myLat = default_lat
        myLon = default_lon
    return {
        'forecast': fetch_data(myLat, myLon)
    }


@app.route('/cities/<name>', methods=['GET'])
def get_cities(name):
    city_name = urllib.parse.unquote(name)
    found_cities = dict(
        filter(lambda item: city_name in item[0], cities.items()))
    sorted_cities = dict(
        sorted(found_cities.items(), key=lambda item: item[0]))
    return {
        'cities': list(sorted_cities.values())
    }


@app.route('/forecast/<name>', methods=['GET'])
def get_forecast_by_city(name):
    city_name = urllib.parse.unquote(name)
    target_city = cities[city_name]
    return {
        'forecast': fetch_data(target_city['lat'], target_city['lon'])
    }


@app.route('/location/', methods=['GET'])
def get_forecast_from_location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    return {
        'forecast': fetch_data(lat, lon)
    }


def fetch_data(lat, lon):
    url_str = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,alerts&units=metric&appid={openweathermap_app_key}'.format(
        lat=lat, lon=lon, openweathermap_app_key=openweathermap_app_key)
    with urllib.request.urlopen(url_str) as url:
        result = json.loads(url.read().decode())
    return result
