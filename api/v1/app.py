#!/usr/bin/python3
"""Flask web application"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask import Blueprint
import os
from flask_cors import CORS

"""Create an instance of the Flask application"""
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

"""register the blueprint app_views"""
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def teardown(err):
    """remove the current session"""
    storage.close()


"""Start the Flask application when the script is run directly"""
if __name__ == "__main__":
    host_name = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port_name = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host_name, port=port_name, threaded=True)
