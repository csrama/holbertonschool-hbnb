#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "name":        fields.String(required=True, description="Amenity name"),
    "description": fields.String(description="Description"),
})

def amenity_to_dict(amenity):
    return {
        "id":          amenity.id,
        "name":        amenity.name,
        "description": getattr(amenity, "description", ""),
    }


@api.route("/")
class AmenityList(Resource):

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve all amenities - PUBLIC"""
        return [amenity_to_dict(a) for a in facade.get_all_amenities()], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity created successfully")
    @api.response(403, "Admin access required")
    @jwt_required()
    def post(self):
        """Create amenity - ADMIN ONLY (Task 4)"""
        if not get_jwt().get('is_admin'):
            return {'error': 'Admin access required'}, 403
        try:
            new_amenity = facade.create_amenity(api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        return amenity_to_dict(new_amenity), 201


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):

    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity by ID - PUBLIC"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity_to_dict(amenity), 200

    @api.expect(amenity_model, validate=False)
    @api.response(200, "Amenity updated successfully")
    @api.response(403, "Admin access required")
    @api.response(404, "Amenity not found")
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity - ADMIN ONLY (Task 4)"""
        if not get_jwt().get('is_admin'):
            return {'error': 'Admin access required'}, 403
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        try:
            updated = facade.update_amenity(amenity_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        return amenity_to_dict(updated), 200
