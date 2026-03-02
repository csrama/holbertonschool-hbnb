import unittest
from app import create_app
from app.extensions import db
from app.models.user import User

class TestUsers(unittest.TestCase):

    def setUp(self):
        self.app = create_app("development")
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            admin = User(
                first_name="Admin",
                last_name="User",
                email="admin@test.com",
                is_admin=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def get_admin_token(self):
        response = self.client.post("/api/v1/login", json={
            "email": "admin@test.com",
            "password": "admin123"
        })
        return response.get_json()["access_token"]

    def test_admin_access(self):
        token = self.get_admin_token()

        response = self.client.get(
            "/api/v1/users",
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
