"""
Test suite for Review (Feedback) API endpoints.
Tests CRUD operations, authorization rules, and business logic.
"""
import unittest
import json
from hbnb.app import create_app
from hbnb.app.extensions import db
from hbnb.app.models.user import Account
from hbnb.app.models.place import Property
from hbnb.app.models.review import Feedback
from flask_jwt_extended import create_access_token


class TestReviewAPI(unittest.TestCase):
    """Test cases for Feedback (Review) API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        # Create test users
        self.property_owner = Account(
            first_name='Property',
            last_name='Owner',
            email='owner@reviews.com',
            plain_password='OwnerPass123',
            is_admin=False
        )
        db.session.add(self.property_owner)
        
        self.reviewer = Account(
            first_name='Review',
            last_name='Writer',
            email='reviewer@test.com',
            plain_password='ReviewPass123',
            is_admin=False
        )
        db.session.add(self.reviewer)
        
        self.other_user = Account(
            first_name='Other',
            last_name='User',
            email='other@reviews.com',
            plain_password='OtherPass123',
            is_admin=False
        )
        db.session.add(self.other_user)
        
        self.admin = Account(
            first_name='Admin',
            last_name='User',
            email='admin@reviews.com',
            plain_password='AdminPass123',
            is_admin=True
        )
        db.session.add(self.admin)
        
        # Create test property
        self.property = Property(
            title='Review Test Property',
            description='Property for testing reviews',
            price=150.00,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.property_owner.user_id
        )
        db.session.add(self.property)
        
        # Create test review
        self.review = Feedback(
            text='Great place to stay! Very clean and comfortable.',
            rating=5,
            user_id=self.reviewer.user_id,
            place_id=self.property.property_id
        )
        db.session.add(self.review)
        
        db.session.commit()
        
        # Generate tokens
        self.owner_token = create_access_token(
            identity=self.property_owner.user_id,
            additional_claims={'is_admin': False}
        )
        
        self.reviewer_token = create_access_token(
            identity=self.reviewer.user_id,
            additional_claims={'is_admin': False}
        )
        
        self.other_token = create_access_token(
            identity=self.other_user.user_id,
            additional_claims={'is_admin': False}
        )
        
        self.admin_token = create_access_token(
            identity=self.admin.user_id,
            additional_claims={'is_admin': True}
        )
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # =====================================================
    # GET /api/v1/reviews - List all reviews
    # =====================================================
    
    def test_get_all_reviews_public(self):
        """Test GET /reviews - public access, no auth required"""
        response = self.client.get('/api/v1/reviews/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        
        # Check structure
        review = data[0]
        self.assertIn('id', review)
        self.assertIn('text', review)
        self.assertIn('rating', review)
        self.assertIn('user_id', review)
        self.assertIn('place_id', review)
        self.assertIn('author_details', review)
        self.assertIn('created', review)
        
        # Check content
        self.assertEqual(review['text'], 'Great place to stay! Very clean and comfortable.')
        self.assertEqual(review['rating'], 5)
        self.assertEqual(review['author_details']['email'], 'reviewer@test.com')
    
    def test_get_all_reviews_empty(self):
        """Test GET /reviews when no reviews exist"""
        # Delete existing review
        db.session.delete(self.review)
        db.session.commit()
        
        response = self.client.get('/api/v1/reviews/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
    
    # =====================================================
    # GET /api/v1/reviews/{id} - Get single review
    # =====================================================
    
    def test_get_single_review_success(self):
        """Test GET /reviews/{id} - existing review"""
        response = self.client.get(f'/api/v1/reviews/{self.review.feedback_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['id'], self.review.feedback_id)
        self.assertEqual(data['text'], 'Great place to stay! Very clean and comfortable.')
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['user_id'], self.reviewer.user_id)
        self.assertEqual(data['place_id'], self.property.property_id)
    
    def test_get_single_review_not_found(self):
        """Test GET /reviews/{id} - non-existent review"""
        response = self.client.get('/api/v1/reviews/non-existent-id')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    # =====================================================
    # GET /api/v1/reviews/places/{place_id}/reviews - Get reviews by place
    # =====================================================
    
    def test_get_reviews_by_place_success(self):
        """Test GET /reviews/places/{place_id}/reviews"""
        response = self.client.get(f'/api/v1/reviews/places/{self.property.property_id}/reviews')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['place_id'], self.property.property_id)
    
    def test_get_reviews_by_place_not_found(self):
        """Test GET /reviews/places/{place_id}/reviews - place not found"""
        response = self.client.get('/api/v1/reviews/places/non-existent-place/reviews')
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_reviews_by_place_empty(self):
        """Test GET /reviews/places/{place_id}/reviews - place with no reviews"""
        # Create new property without reviews
        new_property = Property(
            title='New Property',
            description='No reviews yet',
            price=100.00,
            latitude=34.0522,
            longitude=-118.2437,
            owner_id=self.property_owner.user_id
        )
        db.session.add(new_property)
        db.session.commit()
        
        response = self.client.get(f'/api/v1/reviews/places/{new_property.property_id}/reviews')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])
    
    # =====================================================
    # POST /api/v1/reviews - Create review
    # =====================================================
    
    def test_create_review_success(self):
        """Test POST /reviews - authenticated user creates review"""
        # Create new property for this test
        new_property = Property(
            title='New Property for Review',
            description='Fresh property',
            price=200.00,
            latitude=51.5074,
            longitude=-0.1278,
            owner_id=self.property_owner.user_id
        )
        db.session.add(new_property)
        db.session.commit()
        
        new_review = {
            'text': 'Amazing experience! Would definitely recommend.',
            'rating': 5,
            'user_id': self.reviewer.user_id,
            'place_id': new_property.property_id
        }
        
        response = self.client.post(
            '/api/v1/reviews/',
            json=new_review,
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Amazing experience! Would definitely recommend.')
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['user_id'], self.reviewer.user_id)
        self.assertEqual(data['place_id'], new_property.property_id)
        
        # Verify in database
        review = Feedback.query.filter_by(
            author_id=self.reviewer.user_id,
            property_id=new_property.property_id
        ).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.comment, 'Amazing experience! Would definitely recommend.')
    
    def test_create_review_own_place_forbidden(self):
        """Test POST /reviews - user cannot review their own place"""
        new_review = {
            'text': 'My own place is great!',
            'rating': 5,
            'user_id': self.property_owner.user_id,  # Owner of the property
            'place_id': self.property.property_id
        }
        
        response = self.client.post(
            '/api/v1/reviews/',
            json=new_review,
            headers={'Authorization': f'Bearer {self.owner_token}'}
        )
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn('Cannot review your own property', str(data))
    
    def test_create_duplicate_review_forbidden(self):
        """Test POST /reviews - user cannot review same place twice"""
        new_review = {
            'text': 'Trying to review again',
            'rating': 4,
            'user_id': self.reviewer.user_id,  # Already reviewed this place
            'place_id': self.property.property_id
        }
        
        response = self.client.post(
            '/api/v1/reviews/',
            json=new_review,
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn('already submitted a review', str(data))
    
    def test_create_review_unauthorized(self):
        """Test POST /reviews - no auth token"""
        new_review = {
            'text': 'Great place!',
            'rating': 5,
            'user_id': self.reviewer.user_id,
            'place_id': self.property.property_id
        }
        
        response = self.client.post('/api/v1/reviews/', json=new_review)
        
        self.assertEqual(response.status_code, 401)  # Unauthorized
    
    def test_create_review_wrong_user_id(self):
        """Test POST /reviews - user_id doesn't match authenticated user"""
        new_review = {
            'text': 'Great place!',
            'rating': 5,
            'user_id': self.other_user.user_id,  # Different user
            'place_id': self.property.property_id
        }
        
        response = self.client.post(
            '/api/v1/reviews/',
            json=new_review,
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        self.assertEqual(response.status_code, 401)
    
    def test_create_review_place_not_found(self):
        """Test POST /reviews - place doesn't exist"""
        new_review = {
            'text': 'Great place!',
            'rating': 5,
            'user_id': self.reviewer.user_id,
            'place_id': 'non-existent-place'
        }
        
        response = self.client.post(
            '/api/v1/reviews/',
            json=new_review,
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_create_review_invalid_rating(self):
        """Test POST /reviews - invalid rating value"""
        new_review = {
            'text': 'Great place!',
            'rating': 10,  # Invalid rating (should be 1-5)
            'user_id': self.reviewer.user_id,
            'place_id': self.property.property_id
        }
        
        response = self.client.post(
            '/api/v1/reviews/',
            json=new_review,
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        self.assertEqual(response.status_code, 400)
    
    # =====================================================
    # PUT /api/v1/reviews/{id} - Update review
    # =====================================================
    
    def test_update_own_review_success(self):
        """Test PUT /reviews/{id} - author updates their review"""
        updates = {
            'text': 'Updated review text - even better than I remembered!',
            'rating': 4
        }
        
        response = self.client.put(
            f'/api/v1/reviews/{self.review.feedback_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['text'], 'Updated review text - even better than I remembered!')
        self.assertEqual(data['rating'], 4)
        
        # Verify in database
        db.session.refresh(self.review)
        self.assertEqual(self.review.comment, 'Updated review text - even better than I remembered!')
        self.assertEqual(self.review.score, 4)
    
    def test_update_own_review_partial(self):
        """Test PUT /reviews/{id} - author updates only rating"""
        updates = {'rating': 3}
        
        response = self.client.put(
            f'/api/v1/reviews/{self.review.feedback_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['rating'], 3)
        self.assertEqual(data['text'], 'Great place to stay! Very clean and comfortable.')  # Unchanged
    
    def test_update_other_user_review_forbidden(self):
        """Test PUT /reviews/{id} - different user cannot update"""
        updates = {'text': 'Hacked review'}
        
        response = self.client.put(
            f'/api/v1/reviews/{self.review.feedback_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.other_token}'}
        )
        
        self.assertEqual(response.status_code, 403)
    
    def test_update_review_admin_success(self):
        """Test PUT /reviews/{id} - admin can update any review"""
        updates = {'text': 'Admin updated this review'}
        
        response = self.client.put(
            f'/api/v1/reviews/{self.review.feedback_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Admin updated this review')
    
    def test_update_review_not_found(self):
        """Test PUT /reviews/{id} - review not found"""
        updates = {'text': 'Test'}
        
        response = self.client.put(
            '/api/v1/reviews/non-existent',
            json=updates,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_update_review_cannot_change_user_or_place(self):
        """Test PUT /reviews/{id} - cannot change user_id or place_id"""
        updates = {
            'user_id': self.other_user.user_id,
            'place_id': 'different-place'
        }
        
        response = self.client.put(
            f'/api/v1/reviews/{self.review.feedback_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        # Should succeed but ignore protected fields
        self.assertEqual(response.status_code, 200)
        
        # Verify fields unchanged
        db.session.refresh(self.review)
        self.assertEqual(self.review.author_id, self.reviewer.user_id)
        self.assertEqual(self.review.property_id, self.property.property_id)
    
    # =====================================================
    # DELETE /api/v1/reviews/{id} - Delete review
    # =====================================================
    
    def test_delete_own_review_success(self):
        """Test DELETE /reviews/{id} - author deletes their review"""
        response = self.client.delete(
            f'/api/v1/reviews/{self.review.feedback_id}',
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('success', str(data).lower())
        
        # Verify deleted
        deleted = Feedback.query.get(self.review.feedback_id)
        self.assertIsNone(deleted)
    
    def test_delete_other_user_review_forbidden(self):
        """Test DELETE /reviews/{id} - different user cannot delete"""
        response = self.client.delete(
            f'/api/v1/reviews/{self.review.feedback_id}',
            headers={'Authorization': f'Bearer {self.other_token}'}
        )
        
        self.assertEqual(response.status_code, 403)
    
    def test_delete_review_admin_success(self):
        """Test DELETE /reviews/{id} - admin can delete any review"""
        response = self.client.delete(
            f'/api/v1/reviews/{self.review.feedback_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
    
    def test_delete_review_not_found(self):
        """Test DELETE /reviews/{id} - review not found"""
        response = self.client.delete(
            '/api/v1/reviews/non-existent',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_review_unauthorized(self):
        """Test DELETE /reviews/{id} - no auth token"""
        response = self.client.delete(f'/api/v1/reviews/{self.review.feedback_id}')
        
        self.assertEqual(response.status_code, 401)
    
    # =====================================================
    # Business logic tests
    # =====================================================
    
    def test_review_count_updates(self):
        """Test that property review count reflects correctly"""
        # Get property before new review
        response = self.client.get(f'/api/v1/places/{self.property.property_id}')
        data = json.loads(response.data)
        initial_count = len(data.get('guest_reviews', []))
        
        # Create new property for this test
        new_property = Property(
            title='Count Test Property',
            description='Testing review count',
            price=175.00,
            latitude=48.8566,
            longitude=2.3522,
            owner_id=self.property_owner.user_id
        )
        db.session.add(new_property)
        db.session.commit()
        
        # Add review
        new_review = {
            'text': 'First review',
            'rating': 4,
            'user_id': self.reviewer.user_id,
            'place_id': new_property.property_id
        }
        
        self.client.post(
            '/api/v1/reviews/',
            json=new_review,
            headers={'Authorization': f'Bearer {self.reviewer_token}'}
        )
        
        # Check property has review
        response = self.client.get(f'/api/v1/places/{new_property.property_id}')
        data = json.loads(response.data)
        self.assertEqual(len(data.get('guest_reviews', [])), 1)
    
    def test_review_deletion_cascade(self):
        """Test that deleting a property deletes its reviews"""
        # Create property with review
        temp_property = Property(
            title='Temp Property',
            description='Will be deleted',
            price=125.00,
            latitude=41.9028,
            longitude=12.4964,
            owner_id=self.property_owner.user_id
        )
        db.session.add(temp_property)
        db.session.commit()
        
        temp_review = Feedback(
            text='Temporary review',
            rating=4,
            user_id=self.reviewer.user_id,
            place_id=temp_property.property_id
        )
        db.session.add(temp_review)
        db.session.commit()
        
        review_id = temp_review.feedback_id
        
        # Delete property
        self.client.delete(
            f'/api/v1/places/{temp_property.property_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        # Review should be deleted
        deleted_review = Feedback.query.get(review_id)
        self.assertIsNone(deleted_review)


if __name__ == '__main__':
    unittest.main()
