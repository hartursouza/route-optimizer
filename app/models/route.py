from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    modo = db.Column(db.String(20), nullable=False)
    distancia_total = db.Column(db.Float, nullable=False)
    duracao_total = db.Column(db.Float, nullable=False)
    enderecos = db.Column(JSONB, nullable=False)
    criada_em = db.Column(db.DateTime, default=datetime.utcnow)
