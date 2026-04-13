from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, bcrypt
from app.api.v1 import bp_v1
from config import config_dict

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    
    # Enable CORS for all routes
    CORS(app)
    
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    app.register_blueprint(bp_v1, url_prefix="/api/v1")
    
    from app.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
