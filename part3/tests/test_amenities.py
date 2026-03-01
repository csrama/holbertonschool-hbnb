import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity
from flask_jwt_extended import create_access_token

class TestAmenities(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        
        self.admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@test.com',
            password='admin123',
            is_admin=True
        )
        db.session.add(self.admin)
        
        
        self.user = User(
            first_name='Normal',
            last_name='User',
            email='normal@test.com',
            password='password123'
        )
        db.session.add(self.user)
        
        # إنشاء Amenity
        self.amenity = Amenity(
            name='WiFi',
            description='High-speed internet'
        )
        db.session.add(self.amenity)
        db.session.commit()
        
        self.admin_token = create_access_token(identity=str(self.admin.id))
        self.user_token = create_access_token(identity=str(self.user.id))
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_get_all_amenities(self):
        
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_create_amenity_admin(self):
        
        response = self.client.post('/api/v1/amenities/',
            json={
                'name': 'Pool',
                'description': 'Swimming pool'
            },
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Pool')
    
    def test_create_amenity_non_admin(self):
        
        response = self.client.post('/api/v1/amenities/',
            json={
                'name': 'Gym',
                'description': 'Fitness center'
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 403)
    
    def test_update_amenity_admin(self):
        
        response = self.client.put(f'/api/v1/amenities/{self.amenity.id}',
            json={'name': 'Super WiFi'},
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Super WiFi')
    
    def test_delete_amenity_admin(self):
         
        response = self.client.delete(f'/api/v1/amenities/{self.amenity.id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
