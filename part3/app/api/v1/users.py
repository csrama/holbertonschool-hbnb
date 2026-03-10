from flask_restx import Namespace, Resource, fields
from flask import request
from app.models.user import User
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

# Define the namespace
api = Namespace('users', description='User operations')

# Create the facade
facade = HBnBFacade()

# Data model (Schema) for POST
user_model = api.model('User', {
    'first_name': fields.String(required=True, description="User's first name"),
    'last_name': fields.String(required=True, description="User's last name"),
    'email': fields.String(required=True, description="User's email"),
    'password': fields.String(required=True, description="User's password")
})

# ---- Routes ----
@api.route('/')
class UserList(Resource):

    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        data = request.get_json()
        if not data:
            return {"error": "Invalid input"}, 400

        user_dict, status = facade.create_user(data)
        return user_dict, status

    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        # Convert each user to dictionary
        return [user.to_dict() for user in users], 200
