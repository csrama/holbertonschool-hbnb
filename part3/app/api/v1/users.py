#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

facade = HBnBFacade()

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "first_name": fields.String(required=True, description="First name of the user"),
    "last_name":  fields.String(required=True, description="Last name of the user"),
    "email":      fields.String(required=True, description="Email of the user"),
    "password":   fields.String(required=True, description="Password of the user"),
})

user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(description="First name of the user"),
    "last_name":  fields.String(description="Last name of the user"),
    "email":      fields.String(description="Email of the user"),
    "password":   fields.String(description="Password of the user"),
})

def user_to_dict(user):
    """Convert user to dictionary WITHOUT password."""
    return {
        "id":         user.id,
        "first_name": user.first_name,
        "last_name":  user.last_name,
        "email":      user.email,
        "is_admin":   user.is_admin,
    }


@api.route("/")
class UserList(Resource):

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Retrieve a list of users - PUBLIC"""
        return [user_to_dict(u) for u in facade.get_all_users()], 200

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input data")
    @api.response(403, "Admin access required")
    @jwt_required()
    def post(self):
        """Register a new user - ADMIN ONLY"""
        if not get_jwt().get('is_admin', False):
            return {'error': 'Admin access required'}, 403
        try:
            new_user = facade.create_user(api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        return user_to_dict(new_user), 201


@api.route("/<string:user_id>")
class UserResource(Resource):

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID - PUBLIC"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user_to_dict(user), 200

    @api.expect(user_update_model, validate=False)
    @api.response(200, "User updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id):
        """Update user - AUTHENTICATED"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'Cannot modify email or password'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not updated_user:
            return {"error": "User not found"}, 404
        return user_to_dict(updated_user), 200
