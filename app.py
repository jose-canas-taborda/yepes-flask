import os
from flask import Flask, redirect, request, url_for, flash, render_template, send_from_directory, session
from flask_restful import Api, reqparse

from fileinput import filename
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from sqlalchemy import select

from config import config
from endpoints import *
from models import Archivos


def create_app(enviroment):
    UPLOAD_FOLDER = os.path.abspath("./static/media/")
    print(UPLOAD_FOLDER)
    app = Flask(__name__, static_folder='static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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


@app.route('/admin', )
def admin():
    if 'user' in session and session['rol'] == "admin":
        paciente_cedula = request.args.get('paciente', None)
        remisor_cedula = request.args.get('remisor', None)
        #page = int(request.args.get('page', 1))
        if paciente_cedula: 
            pacientes = Usuario.query.filter_by(rol='paciente', cedula=paciente_cedula).paginate(1,1,error_out=False)
        else:
            pacientes = Usuario.query.filter_by(rol='paciente').paginate(1,1,error_out=False)
        if remisor_cedula:
            remisores = Usuario.query.filter_by(rol='medico', cedula=remisor_cedula).paginate(1,1,error_out=False)
        else:
            remisores = Usuario.query.filter_by(rol='medico').paginate(1,1,error_out=False)

        if pacientes.total == 0:
            flash("Búsqueda sin resultados", 'pacientes')
        if remisores.total == 0:
            flash("Búsqueda sin resultados", 'medicos')
            
        return render_template('panel-control.html', title='Admin', remisores=remisores.items, pacientes=pacientes.items)
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
        paciente_cedula = request.args.get('paciente', None)
        remisor_cedula = request.args.get('remisor', None)
        if paciente_cedula: 
            pacientes = Usuario.query.filter_by(rol='paciente', cedula=paciente_cedula).paginate(1,5,error_out=False)
        else:
            pacientes = Usuario.query.filter_by(rol='paciente').paginate(1,5,error_out=False)
        if remisor_cedula:
            remisores = Usuario.query.filter_by(rol='medico', cedula=remisor_cedula).paginate(1,5,error_out=False)
        else:
            remisores = Usuario.query.filter_by(rol='medico').paginate(1,5,error_out=False)

        if pacientes.total == 0:
            flash("Búsqueda sin resultados", 'pacientes')
        if remisores.total == 0:
            flash("Búsqueda sin resultados", 'medicos')
            
        return render_template('vadmlector.html', title='Admin', remisores=remisores.items, pacientes=pacientes.items)
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/editar-lectura')
def editarlectura():
    examen = request.args.get('examen')
    if 'user' in session and session['rol'] == "admin" or "lector":
        archivo = Archivos.query.filter_by(id=examen).first()
        return render_template('veditarlectura.html', title='Editar Lecturas y Exámenes', archivo=archivo)
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/medico')
def vistamedico():
    if 'user' in session and session['rol'] == "admin" or "medico":
        cedula = request.args.get('cedula')
        datos_medico = Usuario.query.filter_by(cedula=cedula).all()
        pacientes_relaciones = Relacion.query.filter_by(cedulaMedico=cedula).all()
        pacientes_relacionados = []
        for relacion in pacientes_relaciones:
            paciente = Usuario.query.filter_by(cedula=relacion.cedulaPaciente).first()
            pacientes_relacionados.append({
                'id': relacion.id,
                'creado': paciente.fechaCreacionUsuario,
                'cedula': paciente.cedula,
                'nombre': paciente.nombre,
                'apellido': paciente.apellido
            })
        return render_template('vmedico.html', title='Panel del Médico', datos=datos_medico, pacientes_relacionados=pacientes_relacionados)
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/paciente')
def vistapaciente():
    if 'user' in session and session['rol'] == "admin" or "paciente":
        cedula = request.args.get('cedula')
        datos_paciente = Usuario.query.filter_by(cedula=cedula).all()
        archivos = Archivos.query.filter_by(cedulaPaciente=cedula).all()
        return render_template('vpaciente.html', title='Paciente', pacientes=datos_paciente, examenes=archivos, cedula=cedula)
    else:
        return "No tiene Permisos para acceder aquí"

@app.route('/editar-paciente')
def editpaciente():
    if 'user' in session and session['rol'] == "admin":
        cedula = request.args.get('cedula')
        datos_paciente = Usuario.query.filter_by(cedula=cedula).all()
        archivos = Archivos.query.filter_by(cedulaPaciente=cedula).all()
        return render_template('admineditarpaciente.html', 
                               title='Editar Paciente', 
                               pacientes=datos_paciente, 
                               examenes=archivos,
                               cedula=cedula)
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
            paciente = Usuario.query.filter_by(cedula=relacion.cedulaPaciente).first()
            pacientes_relacionados.append({
                'id': relacion.id,
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

@app.route('/delete-examen')
def delete_examen():
    id_examen = request.args.get('examen')
    examen_query = Archivos.query.filter_by(id=id_examen)
    examen = examen_query.one()
    cedula = Usuario.query.filter_by(cedula=examen.cedulaPaciente).one().cedula
    examen_query.delete()
    db.session.commit()
    return redirect(url_for('editpaciente', cedula=cedula))


@app.route("/uploader", methods=['POST'])
def uploader():
    if request.method == "POST":
        filename_lectura = ''
        form = request.form
        cedula = form.get('cedula','')
        nombre = form.get('nombreExamen','Examen sin nombre')
        fecha_examen = form.get('FechaExamen','')
        
        f = request.files['examen']
        filename_examen = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_examen))
        
        lectura = request.files['lectura']
        if lectura.filename != '':
            filename_lectura = secure_filename(lectura.filename)
            lectura.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_lectura)) 
        carga = Archivos(cedulaPaciente=cedula, 
                         nombreExamen=nombre, 
                         examen=filename_examen, 
                         Fecha_examen=fecha_examen, 
                         lectura=filename_lectura)
        db.session.add(carga)
        db.session.commit()
        return redirect(url_for('editpaciente', cedula=cedula))

@app.route("/addlectura", methods=['POST'])
def addlectura():
    if request.method == "POST":
        filename_lectura = ''
        form = request.form
        examen = form.get('examen','')
        
        lectura = request.files['lectura']
        if lectura.filename != '':
            filename_lectura = secure_filename(lectura.filename)
            lectura.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_lectura)) 
        carga = Archivos(lectura=filename_lectura)
        db.session.add(carga)
        db.session.commit()
        return redirect(url_for('editarlectura', examen=examen))
    
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

api.add_resource(Autenticacion, '/autenticacion')
api.add_resource(Usuarios, '/usuarios/')
api.add_resource(GetUsuario, '/usuarios/get/<string:usuario_id>')
api.add_resource(NewUsuario, '/usuarios/new')
api.add_resource(DeleteUsuario, '/usuarios/delete')
api.add_resource(DeleteVariosUsuarios, '/usuarios/delete_varios')
api.add_resource(UpdateUsuario, '/usuarios/update')

api.add_resource(AgregarRelacion, '/relaciones/new')
api.add_resource(DeleteRelacion, '/relaciones/delete')
api.add_resource(AgregarArchivo, '/archivos/new')
api.add_resource(DeleteArchivo, '/archivos/delete')
api.add_resource(UpdateArchivo, '/archivos/update')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)