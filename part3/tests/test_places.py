import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from flask_jwt_extended import create_access_token

class TestPlaces(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        

      self.user = User(
            first_name='Owner',
            last_name='User',
            email='owner@test.com',
            password='password123'
        )
        db.session.add(self.user)
        db.session.commit()
        
        
        self.place = Place(
            title='Test Place',
            description='Test Description',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(self.place)
        db.session.commit()
        
        self.user_token = create_access_token(identity=str(self.user.id))
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_place(self):
       
        response = self.client.post('/api/v1/places/',
            json={
                'title': 'New Place',
                'description': 'New Description',
                'price': 150.0,
                'latitude': 34.0522,
                'longitude': -118.2437,
                'owner_id': self.user.id
            },
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'New Place')
    
    def test_create_place_without_auth(self):

      response = self.client.post('/api/v1/places/',
            json={
                'title': 'New Place',
                'price': 150.0,
                'latitude': 34.0522,
                'longitude': -118.2437,
                'owner_id': self.user.id
            }
        )
        self.assertEqual(response.status_code, 401)
    
    def test_get_all_places(self):
        
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_update_own_place(self):
        
        response = self.client.put(f'/api/v1/places/{self.place.id}',
            json={'title': 'Updated Title'},
            headers={'Authorization': f'Bearer {self.user_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Title')

if __name__ == '__main__':
    unittest.main()
