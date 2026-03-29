from datetime import datetime, timezone

from ..extensions import db


class FeedBatch(db.Model):
    __tablename__ = "feed_batches"

    id = db.Column(db.Integer, primary_key=True)
    batch_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    ingredient_source = db.Column(db.String(120), nullable=False)
    quantity_kg = db.Column(db.Float, nullable=False)
    expected_output_kg = db.Column(db.Float, nullable=True)
    production_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="pending")
    notes = db.Column(db.Text, nullable=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "batch_code": self.batch_code,
            "ingredient_source": self.ingredient_source,
            "quantity_kg": self.quantity_kg,
            "expected_output_kg": self.expected_output_kg,
            "production_date": self.production_date.isoformat(),
            "status": self.status,
            "notes": self.notes,
            "farm_id": self.farm_id,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }
