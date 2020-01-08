from flask import Flask, render_template, request
from map import Map

app = Flask(__name__)


@app.route('/')
def index():
    """Return main map page"""
    return render_template('home.html')


@app.route('/map')
def show_map():
    """Create and display map based on user-input settings"""
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

    map = Map(length, width, f_chance, ri_chance, ro_chance, b_chance)
    print(map)
    return render_template('map.html', map=map)
