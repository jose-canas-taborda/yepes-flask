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
parser_usuario.add_argument('id_usuarios', location='form', type=str)
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
                return redirect("/medico?cedula={}".format(cedula))

            if session['rol'] == 'paciente':
                return redirect("/paciente?cedula={}".format(cedula))
            
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
            rol=args['rol'])
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

class DeleteVariosUsuarios(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        response = ""
        usuarios = args['id_usuarios'].tolist()
        print(args['id_usuarios'])
        for usuario in usuarios:
            usuarioDel = Usuario.query.get(usuario.id)

            if usuarioDel is None:
                response = "Usuario No encontrado"
            else:
                db.session.delete(usuarioDel)
                db.session.commit()
                response = "Usuario con ID: {}".format(usuarioDel.id)

            print(response)
        return "Usuarios Eliminados"

class DeleteRelacion(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        relacion = Relacion.query.get(args['id'])
        if relacion is None:
            response = {'usuario_info': 'Relacion not found'}, 201
        else:
            db.session.delete(relacion)
            db.session.commit()
            response = {'usuario_info': 'Relacion with id {} deleted'.format(args['id'])}, 201
        return response

class DeleteArchivo(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        archivo = Archivos.query.get(args['id'])
        if archivo is None:
            response = {'usuario_info': 'Archivo not found'}, 201
        else:
            db.session.delete(archivo)
            db.session.commit()
            response = {'usuario_info': 'Archivo with id {} deleted'.format(args['id'])}, 201
        return response

class UpdateUsuario(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        usuario = Usuario.query.filter_by(cedula=args['cedula']).first()
        if usuario is None:
            response = {'usuario_info': 'No se encuentra ese Número (cédula) de usuario'}, 201
        else:
            usuario.nombre = args['nombre']
            usuario.apellido = args['apellido']
            usuario.tipoDocumento = args['tipoDocumento']
            usuario.fechaNacimiento = args['fechaNacimiento']
            usuario.telefono = args['telefono']
            usuario.direccion = args['direccion']
            usuario.email1 = args['email1']
            usuario.email2 = args['email2']
            usuario.rol = args['rol']
            db.session.commit()
            usuarios_json = usuario.to_json()
            response = {'usuario_info': usuarios_json}, 201
        if  usuario.rol == "paciente":
            return redirect("/editar-paciente?cedula={}".format(usuario.cedula))
        else:
            return redirect("/editar-medico?cedula={}".format(usuario.cedula))




class AgregarRelacion(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        relaciones = Relacion.query.filter_by(cedulaPaciente=args['cedulaPaciente']).all()
        if relaciones:
            return "Error: El paciente ya está asignado a un médico."
        else:
            relacion = Relacion(
                cedulaMedico=args['cedulaMedico'], cedulaPaciente=args['cedulaPaciente'])
            db.session.add(relacion)
            db.session.commit()
            return "Relacion creada"

class ListaArchivos(Resource):
    def get(self):
        archivos = Archivos.query.all()
        archivos_json = [archivo.to_json() for archivo in archivos]
        response = {'archivos_info': archivos_json}, 201
        return  response

class GetUsuarioArchivos(Resource):
    def get(self, cedula_paciente):
        args = parser_usuario.parse_args()
        archivos = Archivos.query.filter_by(cedulaPaciente=cedula_paciente).all()
        archivos_json = [archivo.to_json() for archivo in archivos]
        response = {'archivos_info': archivos_json}, 201
        return  response

class AgregarArchivo(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        archivos = Archivos(
            cedulaPaciente=args['cedulaPaciente'], examen=args['examen'],
            lectura=args['lectura'], Fecha_examen=args['fechaExamen'], nombreExamen=args['nombreExamen'])      
        db.session.add(archivos)
        db.session.commit()


class AgregarArchivoLectura(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        lectura = Archivos.query.get(args['id'])
        if lectura is None:
            response = {'usuario_info': 'Lectura not found'}, 201
        else:
            lectura.nombre = args['nombre']
            lectura.apellido = args['apellido']
            db.session.commit()
            lectura_json = lectura.to_json()
            response = {'usuario_info': lectura_json}, 201
        return response


class UpdateArchivo(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        lectura = Archivos.query.get(args['id'])
        if lectura is None:
            response = {'usuario_info': 'Lectura not found'}, 201
        else:
            lectura.nombre = args['nombre']
            lectura.fecha = args['Fecha_examen']
            db.session.commit()
            lectura_json = lectura.to_json()
            response = {'usuario_info': lectura_json}, 201
        return response

