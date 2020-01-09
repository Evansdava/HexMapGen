from flask import Flask, render_template, request
import requests
import os
import redis
from map import Map

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)
app = Flask(__name__)


@app.route('/')
def index():
    """Return main map page"""
    return render_template('home.html')


@app.route('/map')
def show_map():
    """Create and display map based on user-input settings"""
    r = requests.get("http://uzby.com/api.php", {'min': 3, 'max': 12})

    name = str(r.content.decode("utf-8"))
    length = request.args.get('length')
    width = request.args.get('width')
    f_chance = request.args.get('f_chance')
    ri_chance = request.args.get('ri_chance')
    ro_chance = request.args.get('ro_chance')
    b_chance = request.args.get('b_chance')

    if length == "" or length is None:
        length = 15
    if width == "" or width is None:
        width = 15
    if f_chance == "" or f_chance is None:
        f_chance = 0.10
    if ri_chance == "" or ri_chance is None:
        ri_chance = 0.02
    if ro_chance == "" or ro_chance is None:
        ro_chance = 0.02
    if b_chance == "" or b_chance is None:
        b_chance = 0.20

    map = Map(name, length, width, f_chance, ri_chance, ro_chance, b_chance)
    print(map)
    return render_template('map.html', map=map)


# @app.route('/map/save/<map_name>')
# def save_map(map_name):
#     """Save the current map to the redis database"""
#     redis.set(map_name, map)