from datetime import datetime, timezone

from ..extensions import db


class Farm(db.Model):
    __tablename__ = "farms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    location = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    users = db.relationship("User", backref="farm", lazy=True)
    feed_batches = db.relationship("FeedBatch", backref="farm", lazy=True)
    monitoring_records = db.relationship("MonitoringRecord", backref="farm", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }
