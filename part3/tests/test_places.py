import unittest
from app import create_app
from app.extensions import db
from app.models.user import User

class TestPlaces(unittest.TestCase):

    def setUp(self):
        self.app = create_app("development")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            user = User(
                first_name="Place",
                last_name="Owner",
                email="owner@test.com"
            )
            user.set_password("123456")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def get_token(self):
        response = self.client.post("/api/v1/login", json={
            "email": "owner@test.com",
            "password": "123456"
        })
        return response.get_json()["access_token"]

    def test_create_place_requires_auth(self):
        response = self.client.post("/api/v1/places", json={
            "title": "Test Place",
            "price": 100
        })

        self.assertEqual(response.status_code, 401)

    def test_create_place_success(self):
        token = self.get_token()

        response = self.client.post(
            "/api/v1/places",
            json={
                "title": "Test Place",
                "price": 100
            },
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 201)
