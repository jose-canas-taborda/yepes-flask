from flask import request, session, redirect
from models import Archivos, Relacion, db
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
parser_usuario.add_argument('nombreExamen', location='form', type=str)
parser_usuario.add_argument('lectura', location='form', type=str)
parser_usuario.add_argument('fechaCreacionUsuario', location='form', type=str)

parser_usuario.add_argument('cedulaMedico', location='form', type=str)
parser_usuario.add_argument('cedulaPaciente', location='form', type=str)

# API Resources
class Autenticacion(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        cedula = args['cedula']
        password = args['password']
        loginInfo = Usuario.query.filter_by(cedula=cedula, password=password).first()
        if loginInfo:
            login_json = loginInfo.to_json()
            session['user'] = args['cedula']
            session['password'] = args['password']
            session['rol'] = login_json['rol']
            if session['rol'] == 'admin':
                return redirect("/admin")
            
            if session['rol'] == 'lector':
                return redirect("/medico-lector")

            if session['rol'] == 'medico':
                return redirect("/medico")

            if session['rol'] == 'paciente':
                return redirect("/paciente")
            
            print("loginInfo:")
            print(login_json['rol'])
            print("session:")
            print(session)
            
        else:
            session.clear()
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
            id=args['id'], tipoDocumento=args['tipoDocumento'], cedula=args['cedula'], 
            password=args['password'], nombre=args['nombre'], apellido=args['apellido'],
            fechaNacimiento=args['fechaNacimiento'], direccion=args['direccion'], 
            telefono=args['telefono'], email1=args['email1'], email2=args['email2'], 
            rol=args['rol'], examen=args['examen'], fechaExamen=args['fechaExamen'],
            lectura=args['lectura'])
        db.session.add(usuario)
        db.session.commit()
        # despues de guardar los datos redirecciona al panel para ver los usuarios creados
        return redirect("/admin")
        #usuarios_json = usuario.to_json()
        #response = {'usuarios_info': usuarios_json}, 201
        #return response

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


class AgregarRelacion(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        relacion = Relacion(
            cedulaMedico=args['cedulaMedico'], cedulaPaciente=args['cedulaPaciente'])
        db.session.add(relacion)
        db.session.commit()


class AgregarArchivo(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        archivos = Archivos(
            cedulaPaciente=args['cedulaPaciente'], examen=args['examen'],
            lectura=args['lectura'], Fecha_examen=args['fechaExamen'], nombreExamen=args['examen'])      
        db.session.add(archivos)
        db.session.commit()

