from flask import Flask, render_template, request, redirect, url_for
import requests
import os
import pickle
import redis
from map import Map

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)
app = Flask(__name__)

current_map = None


@app.route('/')
def index():
    """Return main map page"""
    return render_template('home.html')


@app.route('/map')
def show_map():
    """Create and display map based on user-input settings"""
    global current_map
    r = requests.get("http://uzby.com/api.php", {'min': 3, 'max': 15})

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

    current_map = Map(name, length, width, f_chance,
                      ri_chance, ro_chance, b_chance)
    print(current_map)
    return render_template('map.html', map=current_map)


@app.route('/map/save/<map_name>', methods=["POST"])
def save_map(map_name):
    """Save the current map as a bytestring to the redis database"""
    current_map.name = request.form.get("name")
    byte_map = pickle.dumps(current_map)
    redis.set(current_map.name, byte_map)
    return redirect(url_for('view_map', map_name=current_map.name))


@app.route('/map/<map_name>')
def view_map(map_name):
    """View the requested map"""
    global current_map
    current_map = pickle.loads(redis.get(map_name))
    print(current_map)
    return render_template('show_map.html', map=current_map)


@app.route('/map/delete/<map_name>')
def delete_map(map_name):
    """Delete a map"""
    redis.delete(map_name)
    return redirect(url_for('index'))


@app.route('/list')
def list_maps():
    """View all saved maps"""
    iterator = redis.scan_iter()
    name_list = [key.decode("utf-8") for key in iterator]

    map_list = []
    for name in name_list:
        map_list.append(pickle.loads(redis.get(name)))

    return render_template('map_list.html', maps=map_list)


@app.route('/map/edit/<map_name>', methods=["POST"])
def edit_map(map_name):
    """Edit the name of a map and save it"""
    global current_map
    current_map.name = request.form.get("name")
    # redis.rename(map_name, current_map.name)
    redis.set(current_map.name, pickle.dumps(current_map))
    redis.delete(map_name)
    print(current_map.name)
    return redirect(url_for('view_map', map_name=current_map.name))
