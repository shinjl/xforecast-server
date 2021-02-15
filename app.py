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
# Get default IP from environment file, default IP is used when running the server on the localhost
default_ip = os.environ.get("DEFAULT_IP")

app = Flask(__name__)
CORS(app)

print('app started.')
print(openweathermap_app_key)

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
    if (ip == '127.0.0.1' or ip == 'localhost'):
        ip = default_ip
    url_str = 'http://api.ipstack.com/{ip}?access_key={ipstack_access_key}'.format(
        ip=ip, ipstack_access_key=ipstack_access_key)
    with urllib.request.urlopen(url_str) as url:
        result = json.loads(url.read().decode())

    return {
        'forecast': fetch_data(result['latitude'], result['longitude'])
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
