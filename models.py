from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(10), nullable=False, unique=True) 
    nombre = db.Column(db.String(20), nullable=False) 
    apellido = db.Column(db.String(20), nullable=False)
    #created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    def to_json(self):
        return {
            'id': self.id,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido
        }