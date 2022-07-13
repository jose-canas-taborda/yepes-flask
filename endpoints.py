from flask import session, redirect
from models import db
from flask_restful import Resource, reqparse

from models import Usuario

# parametros enviados por formularios en post 
parser_usuario = reqparse.RequestParser()

# del logeo
parser_usuario.add_argument('cedula', location='form', type=str)
parser_usuario.add_argument('password', location='form', type=str)

# de nuevo usuario
parser_usuario.add_argument('id', location='form', type=str)
parser_usuario.add_argument('tipoDocumento', location='form', type=str)
parser_usuario.add_argument('nombre', location='form', type=str)
parser_usuario.add_argument('apellido', location='form', type=str)
parser_usuario.add_argument('fechaNacimiento', location='form', type=str)
parser_usuario.add_argument('direccion', location='form', type=str)
parser_usuario.add_argument('telefono', location='form', type=str)
parser_usuario.add_argument('email1', location='form', type=str)
parser_usuario.add_argument('email2', location='form', type=str)
parser_usuario.add_argument('rol', location='form', type=str)
parser_usuario.add_argument('examen', location='form', type=str)
parser_usuario.add_argument('fechaExamen', location='form', type=str)
parser_usuario.add_argument('lectura', location='form', type=str)
parser_usuario.add_argument('fechaCreacionUsuario', location='form', type=str)

# API Resources
class Autenticacion(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        usuario = args['user']
        password = args['password']
        loginInfo = Usuario.query.filter_by(cedula=usuario, password=password).first()
        if loginInfo:
            session['usuario'] = args['user']
            session['password'] = args['password']
            session['role'] = 'admin'
            return redirect("/admin")
        else:
            return redirect("/login-error")

class Usuarios(Resource):
    def get(self):
        usuarios = Usuario.query.all()
        usuarios_json = [usuario.to_json() for usuario in usuarios]
        response = {'usuarios_info': usuarios_json}, 201
        return  response

class GetUsuario(Resource):
    def get(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        usuario_json = usuario.to_json()
        response = {'usuario_info': usuario_json}, 201
        return  response

class NewUsuario(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        usuario = Usuario(
            id=args['id'], tipoDocument=args['tipoDocumento'], cedula=args['cedula'], 
            password=args['password'], nombre=args['nombre'], apellido=args['apellido'],
            fechaNacimiento=args['fechaNacimiento'], direccion=args['direccion'], 
            telefono=args['telefono'], email1=args['email1'], email2=args['email2'], 
            rol=args['rol'], examen=args['examen'], fechaExamen=args['fechaexamen'],
            lectura=args['lectura'])
        db.session.add(usuario)
        db.session.commit()
        usuarios_json = usuario.to_json()
        response = {'usuarios_info': usuarios_json}, 201
        return response

class DeleteUsuario(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        usuario = Usuario.query.get(args['id'])
        if usuario is None:
            response = {'usuario_info': 'Usuario not found'}, 201
        else:
            db.session.delete(usuario)
            db.session.commit()
            response = {'usuario_info': 'Usuario with id {} deleted'.format(args['id'])}, 201
        return response

class UpdateUsuario(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        usuario = Usuario.query.get(args['id'])
        if usuario is None:
            response = {'usuario_info': 'Usuario not found'}, 201
        else:
            usuario.nombre = args['nombre']
            usuario.apellido = args['apellido']
            db.session.commit()
            usuarios_json = usuario.to_json()
            response = {'usuario_info': usuarios_json}, 201
        return response



