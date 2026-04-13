"""Review API endpoints for HBnB application"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()


def is_admin():
    """Helper function to check if the current user is an admin"""
    claims = get_jwt()
    return claims.get('is_admin', False)


def review_to_dict(review):
    """Convert review object to dictionary"""
    user_name = None
    if hasattr(review, 'user') and review.user:
        user_name = review.user.get_full_name()

    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user_id,
        'user_name': user_name,
        'place_id': review.place_id,
        'created_at': review.created_at.isoformat() if review.created_at else None,
        'updated_at': review.updated_at.isoformat() if review.updated_at else None
    }


# Define the review model for input validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text', min_length=1),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'place_id': fields.String(required=True, description='Place ID being reviewed')
})

# Define the review response model
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating'),
    'user_id': fields.String(description='User ID'),
    'user_name': fields.String(description='Reviewer Name'),
    'place_id': fields.String(description='Place ID'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})


@api.route('/')
class ReviewList(Resource):
    """Handles operations on the review collection"""

    @api.doc('list_reviews')
    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_response_model)
    def get(self):
        """Get list of all reviews - PUBLIC"""
        reviews = facade.get_all_reviews()
        return [review_to_dict(r) for r in reviews], 200

    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Cannot review your own place or duplicate review')
    @api.response(404, 'User or Place not found')
    @jwt_required()
    def post(self):
        """Create a new review (requires authentication)"""
        review_data = api.payload
        
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        
        # Enforce user_id equals current_user_id
        review_data['user_id'] = current_user_id

        # Validate user exists
        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 404

        # Validate place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Prevent users from reviewing their own places
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 403
        
        # Prevent duplicate reviews - check if user already reviewed this place
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for review in existing_reviews:
            if review.user_id == current_user_id:
                return {'error': 'You have already reviewed this place'}, 403

        try:
            new_review = facade.create_review(review_data)
            return review_to_dict(new_review), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Handles operations on a single review"""

    @api.doc('get_review')
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """Get review details by ID - PUBLIC"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')
        return review_to_dict(review), 200

    @api.doc('update_review')
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized to modify this review')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Update review information (requires authentication and ownership)"""
        review_data = api.payload
        
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()

        # Check if review exists
        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404
        
        # Check if the current user is the author of the review or is admin
        if existing_review.user_id != current_user_id and not is_admin():
            return {'error': 'Unauthorized: You can only modify your own reviews'}, 403

        try:
            updated_review = facade.update_review(review_id, review_data)
            return review_to_dict(updated_review), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.doc('delete_review')
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized to delete this review')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (requires authentication and ownership)"""
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check if the current user is the author of the review or is admin
        if review.user_id != current_user_id and not is_admin():
            return {'error': 'Unauthorized: You can only delete your own reviews'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<string:place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    """Handles operations for reviews of a specific place"""

    @api.doc('get_place_reviews')
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_list_with(review_response_model)
    def get(self, place_id):
        """Get all reviews for a specific place - PUBLIC"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        reviews = facade.get_reviews_by_place(place_id)
        return [review_to_dict(r) for r in reviews], 200
