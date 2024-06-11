#!/usr/bin/python3
"""
Starts API
"""

from flask import Flask
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
def 404_notfound(error):
  return jsonify({"error": "Not Found"}), 404

if __name__ == '__main__':
  app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
