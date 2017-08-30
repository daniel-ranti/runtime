import os
from datetime import datetime, time

import arrow
import requests
import geocoder

FORECAST_KEY = os.environ.get('FORECAST_KEY')
TEMPLATE_URL = 'https://api.darksky.net/forecast/{key}/{lat},{lon}?exclude=minutely,daily,alerts,flags'


def _get_lat_lon(address_string):
	lat_lon_data = geocoder.google(address_string)
	if not lat_lon_data.ok:
		print 'Google API request returns error code: {}'.format(lat_lon_data.error)
		return None
	lat,lon = lat_lon_data.latlng
	return lat,lon


def _get_hourly_data(lat, lon):
	"""hits the darksky API to return the hourly data for the next 24 hours"""
	api_url = TEMPLATE_URL.format(key=FORECAST_KEY, lat=lat, lon=lon)
	weather_response = requests.get(api_url)
	if not weather_response.ok:
		print 'DarkSky API requests returns status code {}'.format(weather_response.status_code)
		return None
	return weather_response.json()['hourly']['data'][:24]


def _calc_runtime_score(weather_by_hour):
	"""Given a single hour of weather returns a score for how ideal that hour will be to run"""
	# TODO: elaborate on this function. 
	ideal_temperature = 50
	runtime_score = abs(weather_by_hour['apparentTemperature'] - ideal_temperature)
	return runtime_score


def _convert_hourly_weather(weather_by_hour):
	"""Takes a single hour of weather and modifys it in place to output format for API (sorry)"""
	# TODO: use lat/lon to figure out timezone. good luck.
	weather_by_hour['time'] = datetime.strptime(str(arrow.get(weather_by_hour['time']).to('EST')), '%Y-%m-%dT%H:%M:%S-05:00')
	return weather_by_hour


def get_best_times(address_string):
	"""Returns the hourly data for the best 3 times to start your run today""" 
  	lat,lon = _get_lat_lon(address_string)
	hourly_data = _get_hourly_data(lat, lon)
	if not hourly_data:
		return []
	converted_data = [_convert_hourly_weather(hw) for hw in hourly_data]
	filtered_data = list(filter(lambda d: time(5,0) < d['time'].time() < time(20,0), converted_data))
	sorted_data = sorted(filtered_data, key=lambda x: _calc_runtime_score(x))
	output = sorted_data[:3]
	return output
