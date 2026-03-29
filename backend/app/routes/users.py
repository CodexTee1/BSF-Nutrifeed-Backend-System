from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from ..models import User


users_bp = Blueprint("users", __name__)


@users_bp.get("")
@jwt_required()
def list_users():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Only admins can view all users"}), 403

    role = request.args.get("role", type=str)
    farm_id = request.args.get("farm_id", type=int)
    active = request.args.get("active", type=str)

    query = User.query
    if role:
        query = query.filter(User.role == role.strip().lower())
    if farm_id is not None:
        query = query.filter(User.farm_id == farm_id)
    if active is not None:
        is_active = active.strip().lower() == "true"
        query = query.filter(User.is_active == is_active)

    users = query.order_by(User.created_at.desc()).all()
    return jsonify({"users": [user.to_dict() for user in users]}), 200
