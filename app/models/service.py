from ..extensions import db

class Service(db.Model):
    __tablename__="services"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco_base = db.Column(db.Float, nullable=False)
    orders = db.relationship("ServiceOrder", backref="service", lazy=True, cascade="all, delete-orphan")
