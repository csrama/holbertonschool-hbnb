from flask import Flask
from flask_restx import Api

from app.extensions import db, bcrypt, jwt
from app.api.v1.auth import auth_bp
from app.api.v1.users import api as users_api
from app.api.v1.places import api as places_api
from app.api.v1.amenities import api as amenities_api
from app.api.v1.reviews import api as reviews_api


# =====================================
# Create App
# =====================================
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'


# =====================================
# Initialize Extensions
# =====================================
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


# =====================================
# Register Blueprints
# =====================================
app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')


# =====================================
# Register APIs
# =====================================
api = Api(app)

api.add_namespace(users_api, path='/api/v1/users')
api.add_namespace(places_api, path='/api/v1/places')
api.add_namespace(amenities_api, path='/api/v1/amenities')
api.add_namespace(reviews_api, path='/api/v1/reviews')


# =====================================
# Run App
# =====================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=True)
    
