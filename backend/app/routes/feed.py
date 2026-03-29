from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Farm, FeedBatch
from ..utils.http import bad_request, paginated_response, parse_pagination


feed_bp = Blueprint("feed", __name__)
VALID_STATUSES = {"pending", "in_progress", "completed"}


@feed_bp.post("")
@jwt_required()
def create_feed_batch():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Only admins can create feed batches"}), 403

    data = request.get_json() or {}
    required_fields = {"batch_code", "ingredient_source", "quantity_kg", "production_date", "farm_id"}
    missing_fields = sorted(required_fields - data.keys())
    if missing_fields:
        return bad_request(f"Missing fields: {', '.join(missing_fields)}")

    if FeedBatch.query.filter_by(batch_code=data["batch_code"].strip()).first():
        return jsonify({"error": "Batch code already exists"}), 409

    try:
        production_date = date.fromisoformat(data["production_date"])
        quantity_kg = float(data["quantity_kg"])
        expected_output_kg = float(data["expected_output_kg"]) if data.get("expected_output_kg") is not None else None
        farm_id = int(data["farm_id"])
    except (TypeError, ValueError):
        return bad_request("Invalid production_date, quantity_kg, expected_output_kg, or farm_id")

    if quantity_kg <= 0:
        return bad_request("quantity_kg must be greater than 0")
    if expected_output_kg is not None and expected_output_kg < 0:
        return bad_request("expected_output_kg cannot be negative")
    if Farm.query.get(farm_id) is None:
        return bad_request("Selected farm does not exist")

    status = data.get("status", "pending").strip().lower()
    if status not in VALID_STATUSES:
        return bad_request("Invalid status supplied")

    batch = FeedBatch(
        batch_code=data["batch_code"].strip(),
        ingredient_source=data["ingredient_source"].strip(),
        quantity_kg=quantity_kg,
        expected_output_kg=expected_output_kg,
        production_date=production_date,
        status=status,
        notes=data.get("notes"),
        farm_id=farm_id,
        created_by=int(get_jwt_identity()),
    )

    db.session.add(batch)
    db.session.commit()

    return jsonify({"message": "Feed batch created", "feed_batch": batch.to_dict()}), 201


@feed_bp.get("")
@jwt_required()
def list_feed_batches():
    page, per_page = parse_pagination()
    status = request.args.get("status", type=str)
    farm_id = request.args.get("farm_id", type=int)

    query = FeedBatch.query
    if status:
        query = query.filter(FeedBatch.status == status.strip().lower())
    if farm_id is not None:
        query = query.filter(FeedBatch.farm_id == farm_id)

    pagination = query.order_by(FeedBatch.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return paginated_response([batch.to_dict() for batch in pagination.items], pagination, "feed_batches"), 200


@feed_bp.patch("/<int:batch_id>/status")
@jwt_required()
def update_feed_batch_status(batch_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Only admins can update feed batch status"}), 403

    batch = FeedBatch.query.get_or_404(batch_id)
    data = request.get_json() or {}
    status = (data.get("status") or "").strip().lower()
    if status not in VALID_STATUSES:
        return bad_request("A valid status is required")

    batch.status = status
    db.session.commit()
    return jsonify({"message": "Feed batch status updated", "feed_batch": batch.to_dict()}), 200
