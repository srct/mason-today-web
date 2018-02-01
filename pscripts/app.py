from flask import Flask
from parscript import what
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return json.dumps(what())
