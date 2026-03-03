from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['POST'])
def login():
    """
    تسجيل الدخول:
    يستقبل JSON:
    {
        "email": "...",
        "password": "..."
    }
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # تحقق من الباسوورد
    if not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # لو صح، أرجع توكن (يمكنك استخدام JWT لاحقًا)
    return jsonify({"access_token": "dummy-token-for-testing"}), 200
