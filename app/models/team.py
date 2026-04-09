from ..extensions import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    participants = db.relationship("User", backref="team", cascade="all, delete-orphan")
