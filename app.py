import os
from flask import Flask, redirect, request, url_for
from flask_restful import Api
from flask import render_template

from flask import Flask, session
from sqlalchemy import select

from config import config
from endpoints import *

def create_app(enviroment):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(enviroment)
    app.secret_key = 'esto-es-una-clave-muy-secreta!!'

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

app = create_app(config['development'])
api = Api(app)

# Templates
@app.route('/')
def index():
    return render_template('index.html', title='Index')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/admin')
def admin():
    usuarios = Usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios]
    print(usuarios_json)
    return render_template('panel-control.html', title='Admin', datos=usuarios_json)

@app.route('/login-error')
def loginError():
    session.clear()
    #session['usuario'] = None
    #session['password'] = None
    #session['role'] = None
    return "Error de login"

@app.route('/nuevo-usuario')
def nuevoUsuario():
    #if session['role'] == 'admin':
        #pass #return render_template('nuevo-usuario.html', title='Nuevo usuario')
    return render_template('adminaddpaciente.html', title='Nuevo usuario')

@app.route('/agregar-medico')
def addmedico():
    return render_template('adminaddmedico.html', title='Nuevo Remisor')

@app.route('/agregar-paciente')
def addpaciente():
    return render_template('adminaddpaciente.html', title='Nuevo Paciente')

@app.route('/editar-paciente')
def editpaciente():
    return render_template('admineditarpaciente.html', title='Editar Paciente')

@app.route('/medico-lector')
def vistalector():
    return render_template('vadmlector.html', title='Agregar Lecturas y Exámenes')

@app.route('/editar-lectura')
def editarlectura():
    return render_template('veditarlectura.html', title='Editar Lecturas y Exámenes')

@app.route('/medico')
def vistamedico():
    return render_template('vmedico.html', title='Panel del Médico')

@app.route('/paciente')
def vistapaciente():
    return render_template('vpaciente.html', title='Panel del Paciente')

@app.route('/editar-medico/<int:id>')
def updatemedico():
    return render_template('admineditarmedico.html',title='Editar Medico')

@app.route('/logout')
def logout():
    if 'cedula' in session:
     session.pop('cedula')
    return redirect(url_for('login'))

#@app.before_request
def valida_session():
    ruta = request.path
    print(ruta)
    if ruta != '/login' and ruta != '/login-error' and not ruta.startswith("/css") and not ruta.startswith("/images"):
        print('valida session')
        #if 'usuario' not in session or 'password' not in session:
        #    return redirect("/login-error")

api.add_resource(Autenticacion, '/autenticacion')
api.add_resource(Usuarios, '/usuarios/')
api.add_resource(GetUsuario, '/usuarios/get/<string:usuario_id>')
api.add_resource(NewUsuario, '/usuarios/new')
api.add_resource(DeleteUsuario, '/usuarios/delete')
api.add_resource(UpdateUsuario, '/usuarios/update')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)