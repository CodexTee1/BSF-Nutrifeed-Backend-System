from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Farm, User
from ..utils.http import bad_request


auth_bp = Blueprint("auth", __name__)
VALID_ROLES = {"admin", "farmer"}


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}

    required_fields = {"full_name", "email", "password", "role"}
    missing_fields = sorted(required_fields - data.keys())
    if missing_fields:
        return bad_request(f"Missing fields: {', '.join(missing_fields)}")

    role = data["role"].strip().lower()
    if role not in VALID_ROLES:
        return bad_request("Role must be either admin or farmer")

    full_name = data["full_name"].strip()
    email = data["email"].strip().lower()
    password = data["password"]
    phone_number = (data.get("phone_number") or "").strip() or None
    farm_id = data.get("farm_id")

    if len(full_name) < 3:
        return bad_request("Full name must be at least 3 characters long")
    if "@" not in email:
        return bad_request("A valid email address is required")
    if len(password) < 8:
        return bad_request("Password must be at least 8 characters long")
    if role == "farmer" and farm_id is None:
        return bad_request("farm_id is required for farmer accounts")
    if farm_id is not None and Farm.query.get(farm_id) is None:
        return bad_request("Selected farm does not exist")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        role=role,
        farm_id=farm_id,
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    if not email or not password:
        return bad_request("Email and password are required")

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    if not user.is_active:
        return jsonify({"error": "User account is inactive"}), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "email": user.email, "farm_id": user.farm_id},
    )

    return jsonify(
        {
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict(),
        }
    ), 200


@auth_bp.get("/me")
@jwt_required()
def get_current_user():
    user = User.query.get_or_404(int(get_jwt_identity()))
    return jsonify({"user": user.to_dict()}), 200
