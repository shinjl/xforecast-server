# xforecast-server

<img align="right" width="64" height="64" src="./images/logo.png">

The backend service for xForecast, a simple weather forecast app built on Svelte. Provides location based weather forecast with one click. Check [this site](http://xforecast.shinjl.com) for more detail.

## Developing

```bash
# create virtual environment and activate it
virtualenv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# configure environment variables
# copy example config file and change variables
cp .env.example .env
# OPEN_WEATHERMAP_APP_KEY = Your OpenWeatherMap APP KEY (required)
# IPSTACK_ACCESS_KEY = Your IPStack ACCESS KEY (required)
# DEFAULT_LAT = Default latitude (optional)
# DEFAULT_LON = Default longitude (optional)

# start development server
.venv/bin/flask run
```
