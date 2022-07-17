from fileinput import filename
import os
from flask import Flask, redirect, request, url_for, flash
from flask_restful import Api, reqparse
from flask import render_template
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


from flask import Flask, session
from sqlalchemy import select

from config import config
from endpoints import *
from models import Archivos


def create_app(enviroment):
    app = Flask(__name__, static_folder='static')
    app.config['UPLOAD_FOLDER'] = "./uploads"
    app.config.from_object(enviroment)
    app.secret_key = 'Er3z1ns0p0rt4b3!'

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

app = create_app(config['development'])
api = Api(app)


parser_logeo = reqparse.RequestParser()

# del logeo
parser_logeo.add_argument('cedula', location='form', type=str)
parser_logeo.add_argument('password', location='form', type=str)
parser_logeo.add_argument('rol', location='form', type=str)

# Templates
@app.route('/')
def index():
    return render_template('login.html', title='Ingrese sus Datos')

@app.route('/login', methods=["POST"])
def login():
    """if request.method == "POST":
        args = parser_logeo.parse_args()
        cedula = args['cedula']
        password = args['password']
        rol = args['rol']
        session['user'] = cedula
        session['rol'] = rol
        return redirect(url_for('admin'))
    else:
        return "No tiene Permiso, favor verificar datos"
    """
    pass

@app.route('/admin')
def admin():
    if 'user' in session and session['rol'] == "admin":
        remisores = Usuario.query.filter_by(rol='medico').all()
        pacientes = Usuario.query.filter_by(rol='paciente').all()
        flash("Búsqueda sin resultados")
        return render_template('panel-control.html', title='Admin', remisores=remisores, pacientes=pacientes)
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/login-error')
def loginError():
    session.clear()
    flash("Introduzca unos datos válidos")
    return render_template('login.html', title='error')

@app.route('/recuperar-password')
def recuperarpassword():
    return render_template('recover.html', title='Recuperar Contraseña')


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
        cedula = request.args.get('cedula')
        datos_paciente = Usuario.query.filter_by(cedula=cedula).all()
        return render_template('vpaciente.html', title='Panel del Paciente', pacientes=datos_paciente)
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/editar-paciente')
def editpaciente():
    if 'user' in session and session['rol'] == "admin":
        cedula = request.args.get('cedula')
        datos_paciente = Usuario.query.filter_by(cedula=cedula).all()
        archivos = Archivos.query.filter_by(cedulaPaciente=cedula).all()
        return render_template('admineditarpaciente.html', title='Editar Paciente', pacientes=datos_paciente, examenes=archivos)
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/editar-medico')
def updatemedico():
    if 'user' in session and session['rol'] == "admin":
        cedula = request.args.get('cedula')
        datos_medico = Usuario.query.filter_by(cedula=cedula).all()
        pacientes_relaciones = Relacion.query.filter_by(cedulaMedico=cedula).all()
        pacientes_relacionados = []
        for relacion in pacientes_relaciones:
            #print(relacion.cedulaPaciente)
            paciente = Usuario.query.filter_by(cedula=relacion.cedulaPaciente).first()
            pacientes_relacionados.append({
                'creado': paciente.fechaCreacionUsuario,
                'cedula': paciente.cedula,
                'nombre': paciente.nombre,
                'apellido': paciente.apellido
            })
            print(paciente.nombre)
        print(pacientes_relacionados)
        return render_template('admineditarmedico.html',title='Editar Medico', datos=datos_medico, pacientes_relacionados=pacientes_relacionados)
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

api.add_resource(AgregarRelacion, '/relaciones/new')
api.add_resource(AgregarArchivo, '/archivos/new')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)