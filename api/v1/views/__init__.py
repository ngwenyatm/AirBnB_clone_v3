#!/usr/bin/python3
"""views"""

import Blueprint from flask doc

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states.py import *
from api.v1.views.cities.py import *
from api.v1.views.amenities.py import *
from api.v1.views.users.py import *
from api.v1.views.places.py import *
from api.v1.views.places_reviews.py import *
