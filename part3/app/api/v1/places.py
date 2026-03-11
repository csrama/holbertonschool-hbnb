from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

place_model = api.model('Place', {
    'name': fields.String(required=True, description="Place name"),
    'price': fields.Float(required=True, description="Price per night"),
    'latitude': fields.Float(required=True, description="Latitude"),
    'longitude': fields.Float(required=True, description="Longitude"),
    'description': fields.String(required=False, description="Description")
})

@api.route('/')
class PlaceList(Resource):

    @jwt_required()
    @api.expect(place_model)
    def post(self):
        """Create a new place (requires JWT)"""
        data = request.get_json()
        if not data:
            return {"error": "Invalid input"}, 400

        user_id = get_jwt_identity()
        place = facade.create_place(user_id, **data)
        return {
            "id": place.id,
            "name": place.title,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "description": place.description,
            "owner_id": place.owner_id
        }, 201

    def get(self):
        """Retrieve all places"""
        places = facade.places.get_all()
        return [
            {
                "id": p.id,
                "name": p.title,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "description": p.description,
                "owner_id": p.owner_id
            } for p in places
        ], 200
