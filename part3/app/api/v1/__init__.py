# app/api/v1/__init__.py
from flask import Blueprint
from flask_restx import Api

# Import your namespaces
from .users import api as users_ns
from .places import api as places_ns
from .amenities import api as amenities_ns
from .reviews import api as reviews_ns

# Create blueprint
bp_v1 = Blueprint("api_v1", __name__)

# Create RESTX API and attach it to the blueprint
api_v1 = Api(bp_v1, title="HBnB API", version="1.0", description="HBnB API v1")

# Add namespaces with paths
api_v1.add_namespace(users_ns, path="/users")
api_v1.add_namespace(places_ns, path="/places")
api_v1.add_namespace(amenities_ns, path="/amenities")
api_v1.add_namespace(reviews_ns, path="/reviews")
