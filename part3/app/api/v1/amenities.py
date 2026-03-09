from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True),
})
@api.route('/')
class AmenityList(Resource):

    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

    @jwt_required()
    @api.expect(amenity_model)
    def post(self):
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin only'}, 403

        data = request.get_json()
        amenity = facade.create_amenity(**data)
        return amenity.to_dict(), 201
