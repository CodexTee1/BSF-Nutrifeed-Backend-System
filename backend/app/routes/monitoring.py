from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Farm, FeedBatch, MonitoringRecord
from ..utils.http import bad_request, paginated_response, parse_pagination


monitoring_bp = Blueprint("monitoring", __name__)


@monitoring_bp.post("")
@jwt_required()
def create_monitoring_record():
    data = request.get_json() or {}
    required_fields = {"larvae_growth_mm", "input_weight_kg", "output_weight_kg", "observation_date", "farm_id"}
    missing_fields = sorted(required_fields - data.keys())
    if missing_fields:
        return bad_request(f"Missing fields: {', '.join(missing_fields)}")

    try:
        farm_id = int(data["farm_id"])
        feed_batch_id = int(data["feed_batch_id"]) if data.get("feed_batch_id") is not None else None
        larvae_growth_mm = float(data["larvae_growth_mm"])
        input_weight_kg = float(data["input_weight_kg"])
        output_weight_kg = float(data["output_weight_kg"])
        temperature_c = float(data["temperature_c"]) if data.get("temperature_c") is not None else None
        humidity_percent = float(data["humidity_percent"]) if data.get("humidity_percent") is not None else None
        record = MonitoringRecord(
            larvae_growth_mm=larvae_growth_mm,
            input_weight_kg=input_weight_kg,
            output_weight_kg=output_weight_kg,
            temperature_c=temperature_c,
            humidity_percent=humidity_percent,
            observation_date=date.fromisoformat(data["observation_date"]),
            notes=data.get("notes"),
            farm_id=farm_id,
            feed_batch_id=feed_batch_id,
            submitted_by=int(get_jwt_identity()),
        )
    except (TypeError, ValueError):
        return bad_request("Invalid numeric values, ids, or observation_date")

    if larvae_growth_mm < 0 or input_weight_kg < 0 or output_weight_kg < 0:
        return bad_request("Growth and weight values cannot be negative")
    if humidity_percent is not None and not 0 <= humidity_percent <= 100:
        return bad_request("humidity_percent must be between 0 and 100")
    if Farm.query.get(farm_id) is None:
        return bad_request("Selected farm does not exist")
    if feed_batch_id is not None and FeedBatch.query.get(feed_batch_id) is None:
        return bad_request("Selected feed batch does not exist")

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Monitoring record created", "monitoring_record": record.to_dict()}), 201


@monitoring_bp.get("")
@jwt_required()
def list_monitoring_records():
    page, per_page = parse_pagination()
    farm_id = request.args.get("farm_id", type=int)
    feed_batch_id = request.args.get("feed_batch_id", type=int)
    observation_date = request.args.get("observation_date", type=str)

    query = MonitoringRecord.query
    if farm_id is not None:
        query = query.filter(MonitoringRecord.farm_id == farm_id)
    if feed_batch_id is not None:
        query = query.filter(MonitoringRecord.feed_batch_id == feed_batch_id)
    if observation_date:
        try:
            parsed_date = date.fromisoformat(observation_date)
        except ValueError:
            return bad_request("observation_date must be in YYYY-MM-DD format")
        query = query.filter(MonitoringRecord.observation_date == parsed_date)

    pagination = query.order_by(MonitoringRecord.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return paginated_response([record.to_dict() for record in pagination.items], pagination, "monitoring_records"), 200
