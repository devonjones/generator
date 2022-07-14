import time
from flask import Flask, request

from town_names.api import town_names

app = Flask(__name__, static_folder='../build', static_url_path='/')
app.register_blueprint(town_names)

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}


