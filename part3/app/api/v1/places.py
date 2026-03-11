#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "title":       fields.String(required=True, description="Place title"),
    "description": fields.String(description="Description"),
    "price":       fields.Float(required=True,  description="Price per night"),
    "latitude":    fields.Float(required=True,  description="Latitude"),
    "longitude":   fields.Float(required=True,  description="Longitude"),
})

place_update_model = api.model("PlaceUpdate", {
    "title":       fields.String(description="Place title"),
    "description": fields.String(description="Description"),
    "price":       fields.Float(description="Price per night"),
    "latitude":    fields.Float(description="Latitude"),
    "longitude":   fields.Float(description="Longitude"),
})

def place_to_dict(place):
    return {
        "id":          place.id,
        "title":       place.title,
        "description": place.description,
        "price":       place.price,
        "latitude":    place.latitude,
        "longitude":   place.longitude,
        "owner_id":    getattr(place, 'owner_id', None),
    }


@api.route("/")
class PlaceList(Resource):

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve all places - PUBLIC"""
        return [place_to_dict(p) for p in facade.get_all_places()], 200

    @api.expect(place_model, validate=True)
    @api.response(201, "Place created successfully")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self):
        """Create a new place - AUTHENTICATED (Task 3)"""
        place_data = api.payload
        place_data['owner_id'] = get_jwt_identity()
        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return place_to_dict(new_place), 201


@api.route("/<string:place_id>")
class PlaceResource(Resource):

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place by ID - PUBLIC"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place_to_dict(place), 200

    @api.expect(place_update_model, validate=False)
    @api.response(200, "Place updated successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required()
    def put(self, place_id):
        """Update place - AUTHENTICATED + OWNER CHECK (Task 3 & 4)"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner_id = getattr(place, 'owner_id', None)
        if not is_admin and owner_id and owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated = facade.update_place(place_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        return place_to_dict(updated), 200

    @api.response(200, "Place deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required()
    def delete(self, place_id):
        """Delete place - AUTHENTICATED + OWNER CHECK (Task 3 & 4)"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner_id = getattr(place, 'owner_id', None)
        if not is_admin and owner_id and owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200
