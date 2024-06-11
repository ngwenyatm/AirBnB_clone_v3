#!/usr/bin/python3
"""
Starts API
"""

from flask import Flask, jsonify
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def db_teardown(exception):
  """
  Function for teardown
  """
  storage.close()
  
@app.errorhandler(404)
def notfound(error):
  return jsonify({"error": "Not Found"}), 404

if __name__ == '__main__':
  host = os.getenv("HBNB_API_HOST". "0.0.0.0")
  port = int(os.getenv("HBNB_API_PORT", 5000))
  app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
