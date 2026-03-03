from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models.user import User

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['POST'])
def login():
    """
    Login endpoint:
    Accepts JSON payload:
    {
        "email": "user@example.com",
        "password": "password123"
    }

    Returns:
        200 OK with access token if credentials are valid
        400 Bad Request if email or password is missing
        401 Unauthorized if password is invalid
        404 Not Found if user does not exist
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Query the database for the user
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Verify the password
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Return a dummy access token for testing (replace with JWT later)
    return jsonify({"access_token": "dummy-token-for-testing"}), 200
