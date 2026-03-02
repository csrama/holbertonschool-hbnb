from flask import Flask
from config import config_dict
from app.extensions import db, jwt, bcrypt

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    return app
