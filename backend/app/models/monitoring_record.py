from datetime import datetime, timezone

from ..extensions import db


class MonitoringRecord(db.Model):
    __tablename__ = "monitoring_records"

    id = db.Column(db.Integer, primary_key=True)
    larvae_growth_mm = db.Column(db.Float, nullable=False)
    input_weight_kg = db.Column(db.Float, nullable=False)
    output_weight_kg = db.Column(db.Float, nullable=False)
    temperature_c = db.Column(db.Float, nullable=True)
    humidity_percent = db.Column(db.Float, nullable=True)
    observation_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id"), nullable=False)
    feed_batch_id = db.Column(db.Integer, db.ForeignKey("feed_batches.id"), nullable=True)
    submitted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "larvae_growth_mm": self.larvae_growth_mm,
            "input_weight_kg": self.input_weight_kg,
            "output_weight_kg": self.output_weight_kg,
            "temperature_c": self.temperature_c,
            "humidity_percent": self.humidity_percent,
            "observation_date": self.observation_date.isoformat(),
            "notes": self.notes,
            "farm_id": self.farm_id,
            "feed_batch_id": self.feed_batch_id,
            "submitted_by": self.submitted_by,
            "created_at": self.created_at.isoformat(),
        }
