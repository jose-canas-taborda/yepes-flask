import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import render_template

from flask import Flask, session

from config import config
from models import db
from models import Usuario

def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    app.secret_key = 'esto-es-una-clave-muy-secreta'

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

app = create_app(config['development'])
api = Api(app)

# params sent by post for new user
parser_usuario = reqparse.RequestParser()
parser_usuario.add_argument('user', location='form', type=str)
parser_usuario.add_argument('password', location='form', type=str)
parser_usuario.add_argument('id', location='form', type=str)
parser_usuario.add_argument('cedula', location='form', type=str)
parser_usuario.add_argument('nombre', location='form', type=str)
parser_usuario.add_argument('apellido', location='form', type=str)

# Templates
@app.route('/')
def index():
    return render_template('index.html', title='Index')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/nuevo-usuario')
def nuevoUsuario():
    if (session['role'] == 'admin') {
        return render_template('nuevo-usuario.html', title='Nuevo usuario')
    }
    

# API Resources
class Autenticacion(Resource):
    def post(self):
        args = parser_usuario.parse_args()
        session['user'] = args['user']
        session['password'] = args['password']
        session['role'] = 'admin'

        print(session)
        response = {'usuarios_info': {}}, 201
        return response

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
            id=args['id'], cedula=args['cedula'],
            nombre=args['nombre'], apellido=args['apellido'])
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

api.add_resource(Autenticacion, '/login-auth')
api.add_resource(Usuarios, '/usuarios/')
api.add_resource(GetUsuario, '/usuarios/get/<string:usuario_id>')
api.add_resource(NewUsuario, '/usuarios/new')
api.add_resource(DeleteUsuario, '/usuarios/delete')
api.add_resource(UpdateUsuario, '/usuarios/update')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)