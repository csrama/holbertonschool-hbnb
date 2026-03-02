from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={"is_admin": user.is_admin}
    )

    return {"access_token": access_token}, 200
