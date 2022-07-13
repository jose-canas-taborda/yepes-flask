from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    tipoDocumento = db.Column(db.String(20), nullable=False)
    cedula = db.Column(db.String(10), nullable=False, unique=True) 
    password = db.Column(db.String(102), nullable=False) 
    nombre = db.Column(db.String(20), nullable=False) 
    apellido = db.Column(db.String(20), nullable=False)
    fechaNacimiento = db.Column(db.DateTime(), nullable=False)
    direccion = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.Integer(), nullable=False, unique=True)
    email1 = db.Column(db.String(20), nullable=False, unique=True)
    email2 = db.Column(db.String(20), nullable=True)
    rol = db.Column(db.String(20), nullable=True)
    examen = db.Column(db.String(20), nullable=True)
    fechaExamen = db.Column(db.DateTime(), nullable=True)
    lectura = db.Column(db.String(20), nullable=True)
    fechaCreacionUsuario = db.Column(db.DateTime(), nullable=True, default=db.func.current_timestamp())

    def to_json(self):
        return {
            'id': self.id,
            'tipo Documento': self.tipoDocumento,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            #'fecha Nacimiento': self.fechaNacimiento,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email1': self.email1,
            'email2': self.email2,
            'rol': self.rol,
            #'creado': self.fechaCreacionUsuario,
            'examen': self.examen,
            'lectura': self.lectura,

        }