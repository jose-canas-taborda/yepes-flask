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
    app.secret_key = 'Er3z1ns0p0rt4b3!'
    app.config['UPLOAD_FOLDER'] = "static/uploads/"

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

app = create_app(config['development'])
api = Api(app)

# Templates
@app.route('/')
def index():
    return render_template('login.html', title='Ingrese sus Datos')

'''@app.route('/login')
def login():
    return render_template('login.html', title='Login')'''

@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        cedula = request.form['cedula']
        rol = request.form['rol']
        session['user'] = cedula
        session['rol'] = rol
        return redirect(url_for('admin'))
    else:
        return "No tiene Permiso, favor verificar datos"

@app.route('/admin')
def admin():
    if 'user' in session and session['rol'] == "admin":
        usuarios = Usuario.query.all()
        usuarios_json = [usuario.to_json() for usuario in usuarios]
        print(usuarios_json)
        return render_template('panel-control.html', title='Admin', datos=usuarios_json)
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/login-error')
def loginError():
    session.clear()
    #session['usuario'] = None
    #session['password'] = None
    #session['role'] = None
    return "Error de login"

@app.route('/nuevo-usuario')
def nuevoUsuario():
    if 'user' in session and session['rol'] == "admin":
        return render_template('adminaddpaciente.html', title='Nuevo usuario')
    else:
        return "No tiene Permisos para acceder aquí"


@app.route('/agregar-medico')
def addmedico():
    if 'user' in session and session['rol'] == "admin":
        return render_template('adminaddmedico.html', title='Nuevo Remisor')
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/agregar-paciente')
def addpaciente():
    if 'user' in session and session['rol'] == "admin":
        return render_template('adminaddpaciente.html', title='Nuevo Paciente')
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/editar-paciente')
def editpaciente():
    if 'user' in session and session['rol'] == "admin":
        return render_template('admineditarpaciente.html', title='Editar Paciente')
    else:
        return "No tiene Permisos para acceder aquí"
@app.route('/medico-lector')
def vistalector():
    if 'user' in session and session['rol'] == "admin" or "lector":
        return render_template('vadmlector.html', title='Agregar Lecturas y Exámenes')
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/editar-lectura')
def editarlectura():
    if 'user' in session and session['rol'] == "admin" or "lector":
        return render_template('veditarlectura.html', title='Editar Lecturas y Exámenes')
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/medico')
def vistamedico():
    if 'user' in session and session['rol'] == "admin" or "medico":
        return render_template('vmedico.html', title='Panel del Médico')
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/paciente')
def vistapaciente():
    if 'user' in session and session['rol'] == "admin" or "paciente":
        return render_template('vpaciente.html', title='Panel del Paciente')
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/editar-medico')
def updatemedico():
    if 'user' in session and session['rol'] == "admin":
        return render_template('admineditarmedico.html',title='Editar Medico')
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

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