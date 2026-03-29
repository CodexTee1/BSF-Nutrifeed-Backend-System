from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from ..extensions import db
from ..models import Farm


farms_bp = Blueprint("farms", __name__)


@farms_bp.post("")
@jwt_required()
def create_farm():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Only admins can create farms"}), 403

    data = request.get_json() or {}
    required_fields = {"name", "location"}
    missing_fields = sorted(required_fields - data.keys())
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    name = data["name"].strip()
    location = data["location"].strip()
    if not name or not location:
        return jsonify({"error": "Name and location cannot be empty"}), 400

    if Farm.query.filter_by(name=name).first():
        return jsonify({"error": "Farm name already exists"}), 409

    farm = Farm(
        name=name,
        location=location,
        description=(data.get("description") or "").strip() or None,
    )
    db.session.add(farm)
    db.session.commit()

    return jsonify({"message": "Farm created", "farm": farm.to_dict()}), 201


@farms_bp.get("")
@jwt_required()
def list_farms():
    farms = Farm.query.order_by(Farm.name.asc()).all()
    return jsonify({"farms": [farm.to_dict() for farm in farms]}), 200
