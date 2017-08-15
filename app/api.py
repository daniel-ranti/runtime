import os

import arrow
import requests


# TODO: take this out of text
FORECAST_KEY = os.environ.get('FORECAST_KEY')
TEMPLATE_URL = 'https://api.darksky.net/forecast/{key}/{lat},{lon}?exclude=minutely,daily,alerts,flags'


def _get_hourly_data(lat, lon):
	"""hits the darksky API to return the hourly data for the next 24 hours"""
	api_url = TEMPLATE_URL.format(key=FORECAST_KEY, lat=lat, lon=lon)
	response = requests.get(api_url)
	if not response.ok:
		print 'API requests returns status code {}'.format(response.status_code)
		return None
	return response.json()['hourly']['data'][:24]


def _calc_runtime_score(weather_by_hour):
	"""Given a single hour of weather returns a score for how ideal that hour will be to run"""
	# TODO: this function to take in hourly data and it should return some integer where the lower the score the better the run
	ideal_temperature = 50
	runtime_score = abs(weather_by_hour['apparentTemperature'] - ideal_temperature)
	return runtime_score


def _convert_hourly_weather(weather_by_hour):
	"""Takes a single hour of weather and modifys it in place to output format for API (sorry)"""
	# TODO: use lat/lon to figure out timezone. good luck.
	weather_by_hour['time'] = str(arrow.get(weather_by_hour['time']).to('EST'))
	return weather_by_hour


def get_best_times(lat, lon):
	"""Returns the hourly data for the best 3 times to start your run today""" 
	# TODO: make this more than just minimum temp bc that would suck in winter
	# TODO: exclude middle of the night
	# TODO: convert datetime
	hourly_data = _get_hourly_data(lat, lon)
	if not hourly_data:
		return []
	sorted_data = sorted(hourly_data, key=lambda x: _calc_runtime_score(x))
	output = [_convert_hourly_weather(hw) for hw in sorted_data[:3]]
	return output
