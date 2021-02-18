from flask import Flask, request
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

print('xforecast-server service started')


@app.route('/', methods=['GET'])
def index():
    ip = request.remote_addr
    print(ip)
    url_str = 'http://api.ipstack.com/{ip}?access_key={ipstack_access_key}'.format(
        ip=ip, ipstack_access_key=ipstack_access_key)
    with urllib.request.urlopen(url_str) as url:
        result = json.loads(url.read().decode())
    print(result)

    my_lat = result['latitude']
    my_lon = result['longitude']
    if (result['latitude'] is None or result['longitude'] is None):
        my_lat = default_lat
        my_lon = default_lon
    return {
        'forecast': fetch_data(my_lat, my_lon),
        'location': {
            'lat': my_lat,
            'lon': my_lon
        }
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
