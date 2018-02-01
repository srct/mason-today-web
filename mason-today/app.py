from flask import Flask
from parscript import load_data
import json
app = Flask(__name__)

@app.route("/")
def display_data():
    return json.dumps(load_data())
