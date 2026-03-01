from flask import Blueprint
from flask_restx import Api

# Create blueprint
api_bp = Blueprint('api', __name__)

# Create API with blueprint
api = Api(
    api_bp,
    title='HBnB API',
    version='1.0',
    description='HBnB Application API',
    doc='/swagger/'  # Different documentation path
)

# Import and register namespaces
from .auth import api as auth_ns
from .users import api as users_ns
from .places import api as places_ns
from .reviews import api as reviews_ns
from .amenities import api as amenities_ns

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(amenities_ns, path='/amenities')
