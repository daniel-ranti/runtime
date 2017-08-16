import click
from flask import Flask, request, json, render_template

import api 

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_times():
    if request.method == 'POST':
        form_data = request.form 
        lat = form_data.get('lat')
        lon = form_data.get('lon')
        if not (lon and lat):
            # TODO: add an error code
            return json.jsonify({'error':'must provide both lat and lon'})
        best_times = api.get_best_times(lat, lon)
        return render_template('form.html', best_times=best_times)
    else:
        return render_template('form.html')


@click.command()
@click.option('--port', default=5000)
@click.option('--debug', is_flag=True, default=False)
def run_app(port, debug):
    app.debug = debug 
    app.run(port=port)


if __name__ == '__main__':
    run_app()
