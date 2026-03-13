"""Amenity API endpoints for HBnB application"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

facade = HBnBFacade()


def is_admin():
    """Helper function to check if the current user is an admin"""
    claims = get_jwt()
    return claims.get('is_admin', False)


def amenity_to_dict(amenity):
    """Convert amenity object to dictionary"""
    return {
        'id': amenity.id,
        'name': amenity.name,
        'description': getattr(amenity, 'description', ''),
        'created_at': amenity.created_at.isoformat() if amenity.created_at else None,
        'updated_at': amenity.updated_at.isoformat() if amenity.updated_at else None
    }


# Define the amenity model for input validation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name', min_length=1, max_length=50),
    'description': fields.String(description='Amenity description', max_length=200)
})

# Define the amenity response model
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'description': fields.String(description='Amenity description'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})


@api.route('/')
class AmenityList(Resource):
    """Handles operations on the amenity collection"""

    @api.doc('list_amenities')
    @api.response(200, 'List of amenities retrieved successfully')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """Get list of all amenities - PUBLIC"""
        amenities = facade.get_all_amenities()
        return [amenity_to_dict(a) for a in amenities], 200

    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(409, 'Amenity with this name already exists')
    @jwt_required()
    def post(self):
        """Create a new amenity (requires admin privileges)"""
        # Check if user is admin
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload

        # Check if amenity with same name already exists
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity with this name already exists'}, 409

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return amenity_to_dict(new_amenity), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    """Handles operations on a single amenity"""

    @api.doc('get_amenity')
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get amenity details by ID - PUBLIC"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity_to_dict(amenity), 200

    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @api.response(409, 'Amenity with this name already exists')
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity information (requires admin privileges)"""
        # Check if user is admin
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload

        # Check if amenity exists
        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404

        # Check if name is being changed to one that already exists
        if 'name' in amenity_data:
            amenity_with_name = facade.get_amenity_by_name(amenity_data['name'])
            if amenity_with_name and amenity_with_name.id != amenity_id:
                return {'error': 'Amenity with this name already exists'}, 409

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return amenity_to_dict(updated_amenity), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.doc('delete_amenity')
    @api.response(200, 'Amenity deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity (requires admin privileges)"""
        # Check if user is admin
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200
