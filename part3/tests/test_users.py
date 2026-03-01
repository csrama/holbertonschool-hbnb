"""
Test suite for User (Account) API endpoints.
Tests CRUD operations and authorization rules.
"""
import unittest
import json
from hbnb.app import create_app
from hbnb.app.extensions import db
from hbnb.app.models.user import Account
from flask_jwt_extended import create_access_token


class TestUserAPI(unittest.TestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        # Create test admin user
        self.admin = Account(
            first_name='Admin',
            last_name='User',
            email='admin@users.com',
            plain_password='AdminPass123',
            is_admin=True
        )
        db.session.add(self.admin)
        
        # Create test regular user
        self.user = Account(
            first_name='Regular',
            last_name='User',
            email='regular@users.com',
            plain_password='UserPass123',
            is_admin=False
        )
        db.session.add(self.user)
        
        db.session.commit()
        
        # Generate tokens
        self.admin_token = create_access_token(
            identity=self.admin.user_id,
            additional_claims={'is_admin': True}
        )
        
        self.user_token = create_access_token(
            identity=self.user.user_id,
            additional_claims={'is_admin': False}
        )
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # =====================================================
    # GET /api/v1/users - List all users
    # =====================================================
    
    def test_get_all_users_public(self):
        """Test GET /users - public access"""
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should return both users
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        
        # Check structure (no passwords)
        for user in data:
            self.assertIn('id', user)
            self.assertIn('first_name', user)
            self.assertIn('last_name', user)
            self.assertIn('email', user)
            self.assertIn('is_admin', user)
            self.assertNotIn('password', user)
            self.assertNotIn('password_hash', user)
    
    # =====================================================
    # GET /api/v1/users/{id} - Get single user
    # =====================================================
    
    def test_get_single_user_success(self):
        """Test GET /users/{id} - existing user"""
        response = self.client.get(f'/api/v1/users/{self.user.user_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['id'], self.user.user_id)
        self.assertEqual(data['email'], 'regular@users.com')
        self.assertEqual(data['first_name'], 'Regular')
        self.assertEqual(data['last_name'], 'User')
        self.assertFalse(data['is_admin'])
    
    def test_get_single_user_not_found(self):
        """Test GET /users/{id} - non-existent user"""
        response = self.client.get('/api/v1/users/non-existent-id')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    # =====================================================
    # POST /api/v1/users - Create user
    # =====================================================
    
    def test_create_first_user_success(self):
        """Test POST /users - first user (no auth required)"""
        # Clear all users first
        db.session.query(Account).delete()
        db.session.commit()
        
        new_user = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password': 'NewPass123',
            'is_admin': False
        }
        
        response = self.client.post(
            '/api/v1/users/',
            json=new_user
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        
        self.assertIn('id', data)
        self.assertEqual(data['email'], 'new@example.com')
        self.assertEqual(data['first_name'], 'New')
        self.assertEqual(data['last_name'], 'User')
        self.assertFalse(data['is_admin'])
        
        # Verify in database
        user = Account.query.filter_by(email_address='new@example.com').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.verify_password('NewPass123'))
    
    def test_create_user_with_existing_users_requires_admin(self):
        """Test POST /users - with existing users, requires admin"""
        new_user = {
            'first_name': 'Another',
            'last_name': 'User',
            'email': 'another@example.com',
            'password': 'AnotherPass123'
        }
        
        # Try without auth (should fail)
        response = self.client.post('/api/v1/users/', json=new_user)
        self.assertEqual(response.status_code, 403)
        
        # Try with regular user token (should fail)
        response = self.client.post(
            '/api/v1/users/',
            json=new_user,
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 403)
        
        # Try with admin token (should succeed)
        response = self.client.post(
            '/api/v1/users/',
            json=new_user,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 201)
    
    def test_create_user_duplicate_email(self):
        """Test POST /users - duplicate email"""
        new_user = {
            'first_name': 'Duplicate',
            'last_name': 'User',
            'email': 'regular@users.com',  # Already exists
            'password': 'Pass123'
        }
        
        response = self.client.post(
            '/api/v1/users/',
            json=new_user,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 409)  # Conflict
        data = json.loads(response.data)
        self.assertIn('already registered', str(data))
    
    def test_create_user_invalid_email(self):
        """Test POST /users - invalid email format"""
        new_user = {
            'first_name': 'Invalid',
            'last_name': 'Email',
            'email': 'not-an-email',
            'password': 'Pass123'
        }
        
        response = self.client.post(
            '/api/v1/users/',
            json=new_user,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 400)
    
    # =====================================================
    # PUT /api/v1/users/{id} - Update user
    # =====================================================
    
    def test_update_own_profile(self):
        """Test PUT /users/{id} - user updates own profile"""
        updates = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.put(
            f'/api/v1/users/{self.user.user_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['first_name'], 'Updated')
        self.assertEqual(data['last_name'], 'Name')
        self.assertEqual(data['email'], 'regular@users.com')  # Unchanged
        
        # Verify in database
        db.session.refresh(self.user)
        self.assertEqual(self.user.given_name, 'Updated')
        self.assertEqual(self.user.family_name, 'Name')
    
    def test_update_own_profile_cannot_change_admin_flag(self):
        """Test PUT /users/{id} - user cannot change is_admin flag"""
        updates = {'is_admin': True}
        
        response = self.client.put(
            f'/api/v1/users/{self.user.user_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        
        # Should succeed but ignore admin flag
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['is_admin'])
    
    def test_update_other_user_forbidden(self):
        """Test PUT /users/{id} - user cannot update another user"""
        updates = {'first_name': 'Hacked'}
        
        response = self.client.put(
            f'/api/v1/users/{self.admin.user_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        
        self.assertEqual(response.status_code, 401)  # Unauthorized
    
    def test_admin_update_any_user(self):
        """Test PUT /users/{id} - admin can update any user"""
        updates = {
            'first_name': 'AdminUpdated',
            'email': 'newemail@test.com'
        }
        
        response = self.client.put(
            f'/api/v1/users/{self.user.user_id}',
            json=updates,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['first_name'], 'AdminUpdated')
        self.assertEqual(data['email'], 'newemail@test.com')
    
    def test_update_user_not_found(self):
        """Test PUT /users/{id} - user not found"""
        updates = {'first_name': 'Test'}
        
        response = self.client.put(
            '/api/v1/users/non-existent',
            json=updates,
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 404)
    
    # =====================================================
    # DELETE /api/v1/users/{id} - Delete user
    # =====================================================
    
    def test_delete_user_admin_success(self):
        """Test DELETE /users/{id} - admin deletes user"""
        response = self.client.delete(
            f'/api/v1/users/{self.user.user_id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify deleted
        deleted = Account.query.get(self.user.user_id)
        self.assertIsNone(deleted)
    
    def test_delete_user_regular_user_forbidden(self):
        """Test DELETE /users/{id} - regular user cannot delete"""
        response = self.client.delete(
            f'/api/v1/users/{self.user.user_id}',
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        
        self.assertEqual(response.status_code, 403)
    
    def test_delete_user_not_found(self):
        """Test DELETE /users/{id} - user not found"""
        response = self.client.delete(
            '/api/v1/users/non-existent',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
