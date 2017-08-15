import click
from flask import Flask, request, json

import api 

app = Flask(__name__)


@app.route('/')
def get_times():
	query_params = request.args
	lat = query_params.get('lat')
	lon = query_params.get('lon')
	if not (lon and lat):
		# TODO: add an error code
		return json.jsonify({'error':'must provide both lat and lon'})
	best_times = api.get_best_times(lat, lon)
	return json.jsonify({'best_times': best_times})


@click.command()
@click.option('--port', default=5000)
@click.option('--debug', is_flag=True, default=False)
def run_app(port, debug):
	app.debug = debug 
	app.run(port=port)


if __name__ == '__main__':
	run_app()


