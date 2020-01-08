from flask import Flask, render_template
from map import Map

app = Flask(__name__)


@app.route('/')
def index():
    """return main map page"""
    map = Map(29)
    print(map)
    return render_template('map.html', map=map)
