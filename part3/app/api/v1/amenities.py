"""Amenity management endpoints for the HBnB platform"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from hbnb.app.services.facade import HBnBFacade

# Create namespace for amenity operations
amenity_namespace = Namespace('amenities', description='Amenity resource management')

# Initialize service facade
service_facade = HBnBFacade()

def verify_admin_privileges():
    """Check if authenticated user has administrator rights"""
    token_claims = get_jwt()
    return token_claims.get('is_admin', False)

# Request validation schema for amenity creation/update
amenity_input_schema = amenity_namespace.model('AmenityInput', {
    'name': fields.String(
        required=True, 
        description='Amenity display name',
        min_length=2, 
        max_length=50,
        example='WiFi'
    )
})

# Response schema for amenity data
amenity_output_schema = amenity_namespace.model('AmenityOutput', {
    'id': fields.String(description='Unique amenity identifier'),
    'name': fields.String(description='Amenity display name'),
    'created_at': fields.String(description='Timestamp of creation'),
    'updated_at': fields.String(description='Timestamp of last modification')
})

@amenity_namespace.route('/')
class AmenityCollection(Resource):
    """Resource handler for amenity collection endpoints"""
    
    @amenity_namespace.doc('retrieve_all_amenities')
    @amenity_namespace.response(200, 'Successfully retrieved amenity list')
    def get(self):
        """Fetch all available amenities from the system"""
        amenities = service_facade.get_all_amenities()
        
        formatted_response = []
        for amenity in amenities:
            formatted_response.append({
                'identifier': amenity.id,
                'display_name': amenity.name,
                'creation_date': amenity.created_at.isoformat(),
                'modification_date': amenity.updated_at.isoformat()
            })
        
        return formatted_response, 200
    
    @amenity_namespace.doc('register_new_amenity')
    @amenity_namespace.expect(amenity_input_schema)
    @amenity_namespace.response(201, 'Amenity successfully registered')
    @amenity_namespace.response(400, 'Invalid request data')
    @amenity_namespace.response(403, 'Insufficient permissions')
    @amenity_namespace.response(409, 'Amenity name conflict')
    @jwt_required()
    def post(self):
        """Create a new amenity (administrator access only)"""
        # Verify administrator status
        if not verify_admin_privileges():
            amenity_namespace.abort(403, 'Administrator privileges required')
        
        request_data = amenity_namespace.payload
        
        # Check for existing amenity with same name
        existing_amenity = service_facade.get_amenity_by_name(request_data['name'])
        if existing_amenity:
            amenity_namespace.abort(409, 'Amenity name already exists in the system')
        
        try:
            created_amenity = service_facade.create_amenity(request_data)
            
            response_data = {
                'identifier': created_amenity.id,
                'display_name': created_amenity.name,
                'creation_date': created_amenity.created_at.isoformat(),
                'modification_date': created_amenity.updated_at.isoformat()
            }
            
            return response_data, 201
            
        except ValueError as error:
            amenity_namespace.abort(400, str(error))

@amenity_namespace.route('/<amenity_identifier>')
@amenity_namespace.param('amenity_identifier', 'Unique amenity system ID')
class AmenityInstance(Resource):
    """Resource handler for individual amenity operations"""
    
    @amenity_namespace.doc('fetch_single_amenity')
    @amenity_namespace.response(200, 'Successfully retrieved amenity')
    @amenity_namespace.response(404, 'Amenity not found')
    def get(self, amenity_identifier):
        """Retrieve specific amenity details by ID"""
        target_amenity = service_facade.get_amenity(amenity_identifier)
        
        if not target_amenity:
            amenity_namespace.abort(404, 'Amenity not found in the system')
        
        response_data = {
            'identifier': target_amenity.id,
            'display_name': target_amenity.name,
            'creation_date': target_amenity.created_at.isoformat(),
            'modification_date': target_amenity.updated_at.isoformat()
        }
        
        return response_data, 200
    
    @amenity_namespace.doc('modify_existing_amenity')
    @amenity_namespace.expect(amenity_input_schema)
    @amenity_namespace.response(200, 'Amenity successfully updated')
    @amenity_namespace.response(400, 'Invalid modification data')
    @amenity_namespace.response(403, 'Insufficient permissions')
    @amenity_namespace.response(404, 'Amenity not found')
    @amenity_namespace.response(409, 'Amenity name conflict')
    @jwt_required()
    def put(self, amenity_identifier):
        """Update an existing amenity (administrator access only)"""
        # Verify administrator status
        if not verify_admin_privileges():
            amenity_namespace.abort(403, 'Administrator privileges required')
        
        modification_data = amenity_namespace.payload
        
        # Verify amenity exists
        existing_amenity = service_facade.get_amenity(amenity_identifier)
        if not existing_amenity:
            amenity_namespace.abort(404, 'Amenity not found in the system')
        
        # Check for name conflicts
        if 'name' in modification_data:
            name_conflict = service_facade.get_amenity_by_name(modification_data['name'])
            if name_conflict and name_conflict.id != amenity_identifier:
                amenity_namespace.abort(409, 'Amenity name already used by another record')
        
        try:
            updated_amenity = service_facade.update_amenity(amenity_identifier, modification_data)
            
            response_data = {
                'identifier': updated_amenity.id,
                'display_name': updated_amenity.name,
                'creation_date': updated_amenity.created_at.isoformat(),
                'modification_date': updated_amenity.updated_at.isoformat()
            }
            
            return response_data, 200
            
        except ValueError as error:
            amenity_namespace.abort(400, str(error))
