# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    unique_code = db.Column(db.String(100), nullable=False)
    booking_details = db.Column(db.Text, nullable=False)
    time_of_collection = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    status = db.Column(db.String(50), default="Pending")  # Pending, Collected, Expired
    time_of_return = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'Reservation("{self.name}", "{self.unique_code}", "{self.booking_details}", "{self.time_of_collection}", "{self.status}")'

    def is_expired(self):
        if self.status == "Expired":
            return True
        return datetime.now() > (self.time_of_collection + timedelta(minutes=self.duration))
