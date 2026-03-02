import unittest
from app import create_app
from app.extensions import db
from app.models.user import User

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = create_app("development")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            user = User(
                first_name="Test",
                last_name="User",
                email="test@test.com"
            )
            user.set_password("123456")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_login_success(self):
        response = self.client.post("/api/v1/login", json={
            "email": "test@test.com",
            "password": "123456"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json())

    def test_login_fail(self):
        response = self.client.post("/api/v1/login", json={
            "email": "test@test.com",
            "password": "wrong"
        })

        self.assertEqual(response.status_code, 401)
