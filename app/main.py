import click
from flask import Flask, request, json, render_template

import api 

data_error='Please enter an address or location'
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_times():
    if request.method == 'POST':
        form_data = request.form 
        address_string = form_data.get('address_string')
        if not address_string:
            return render_template('form.html', data_error=data_error)
        best_times = api.get_best_times(address_string)
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
