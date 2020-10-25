import os

from flask import Flask, render_template, request

import requests

from requests import ConnectionError

app = Flask(__name__)

URL = "http://www.omdbapi.com/?apikey=" + os.getenv('MY_API_KEY', '')


def get_results(title, year, show_type):
    params = {
        's': title,
        'type': show_type,
        'y': year
    }
    try:
        response = requests.get(URL, params=params).json()
    except ConnectionError:
        return []
    return response.get("Search", [])


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year_input')
        show_type = request.form.get('show_type')
        res = get_results(title, year, show_type)
        return render_template(
            'index.j2',
            results=res
        )
    if request.method == 'GET':
        return render_template('index.j2')


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
