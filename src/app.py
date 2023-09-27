from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from datetime import datetime
import mysql.connector

import os #Permite acceder a los directorios
import database as db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager,logout_user
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import make_response
from flask_paginate import Pagination, get_page_parameter
import re


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,"src", "templates")


app = Flask(__name__, template_folder = template_dir)
# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


#Validaciones
def validar_nombre(nombre):
    if re.match("^[A-Za-z]+$", nombre):
        return True
    else:
        return False
    
def validar_apellido(apellido):
    if re.match("^[A-Za-z]+$", apellido):
        return True
    else:
        return False

def validar_nombre_titular(nombre_titular):
    if re.match("^[A-Za-z]+$", nombre_titular):
        return True
    else:
        return False
    
def validar_nombre_alumno(nombre_alumno):
    if re.match("^[A-Za-z]+$", nombre_alumno):
        return True
    else:
        return False
    
def validar_apellido_alumno(apellido_alumno):
    if re.match("^[A-Za-z]+$", apellido_alumno):
        return True
    else:
        return False

def validar_telefono(telefono):
    # Expresión regular para validar un número de teléfono que contiene solo números y ciertos caracteres especiales como +, -, (, y )
    patron = r"^[0-9+\-() ]+$"
    
    if re.match(patron, telefono):
        return True
    else:
        return False 
    
def validar_telefono_titular(telefono_titular):
    # Expresión regular para validar un número de teléfono que contiene solo números y ciertos caracteres especiales como +, -, (, y )
    patron = r"^[0-9+\-() ]+$"
    
    if re.match(patron, telefono_titular):
        return True
    else:
        return False 
#Rutas
#Resumen
@app.route('/resumen', methods=['GET', 'POST'])
def resumen():
    return render_template('resumen.html')
#login
@app.route('/')
def pagina_inicio():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
        return redirect(url_for('inicio'))

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')

#Home
@app.route('/inicio')
def inicio():
    
    return render_template('inicio.html')

@app.route("/index")
def alta():
    form_data = session.pop('form_data', None)  # Obtener los datos del formulario almacenados en sesión
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM alumnos")
    myresult = cursor.fetchall()
    # Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("index.html", data=insertObject, form_data=form_data)

@app.route("/alumnos", methods=["POST"])
def agregarAlumno():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    fecha_inicio = request.form["fecha_inicio"]
    colegio = request.form["colegio"]
    curso = request.form["curso"]
    nivel_educativo = request.form["nivel_educativo"]
    nombre_titular = request.form["nombre_titular"]
    telefono_titular = request.form["telefono_titular"]
    dia = request.form["dia"]
    horario = request.form["horario"]
    materia = request.form["materia"]

    if not validar_nombre(nombre):
        flash("El nombre no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))
    
    if not validar_telefono(telefono):
        flash("El número de teléfono no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,
        'dia': dia,
        'horario': horario,
        'materia': materia
        }
        return redirect(url_for('alta'))

    if not validar_apellido(apellido):
        flash("El apellido no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))

    if not validar_nombre_titular(nombre_titular):
        flash("El nombre del tutor no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))
    
    if not validar_telefono_titular(telefono_titular):
        flash("El número de teléfono tutor no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,
        'dia': dia,
        'horario': horario,
        'materia': materia
        }
        return redirect(url_for('alta'))

    # Obtén la fecha de nacimiento del formulario
    fecha_nacimiento_str = request.form["fecha_nacimiento"]
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
    # Obtiene la fecha actual
    fecha_actual = datetime.now().date()

    # Compara la fecha de nacimiento con la fecha actual
    if fecha_nacimiento >= fecha_actual:
        flash("La fecha de nacimiento debe ser en el pasado.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento_str,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))

    # Resto del código para agregar el alumno a la base de datos
    cursor = db.database.cursor()
    sql = "INSERT INTO alumnos (nombre, apellido, email, telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular, dia, horario, materia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (nombre, apellido, email, telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular, dia, horario, materia) 
    try:
        cursor.execute(sql, data)
        db.database.commit()  # Realiza el commit después de la inserción
    except mysql.connector.Error as err:
        # Maneja los errores de SQL aquí
        print(f"Error de MySQL: {err}")
    return redirect(url_for('alta'))
   

#Eliminar
@app.route("/eliminar/<string:id>")
def eliminar(id):
    cursor = db.database.cursor()
    sql =  "DELETE FROM alumnos WHERE id = %s"
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('alta'))

# Actualizar
@app.route("/editar/<string:id>", methods=["POST"])
def editar(id):
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    fecha_inicio = request.form["fecha_inicio"]
    colegio = request.form["colegio"]
    curso = request.form["curso"]
    nivel_educativo = request.form["nivel_educativo"]
    nombre_titular = request.form["nombre_titular"]
    telefono_titular = request.form["telefono_titular"]
    dia = request.form["dia"]
    horario = request.form["horario"]
    materia = request.form["materia"]

    if not validar_nombre_titular(nombre_titular):
        flash("El nombre del tutor no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))
    
    if not validar_telefono(telefono):
        flash("El número de teléfono no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,
        'dia': dia,
        'horario': horario,
        'materia': materia
        }
        return redirect(url_for('alta'))
    
    if not validar_telefono_titular(telefono_titular):
        flash("El número de teléfono del tutor no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,
        'dia': dia,
        'horario': horario,
        'materia': materia
        }
        return redirect(url_for('alta'))

    if not validar_nombre(nombre):
        flash("El nombre no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))

    if not validar_apellido(apellido):
        flash("El apellido no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))

    # Obtén la fecha de nacimiento del formulario
    fecha_nacimiento_str = request.form["fecha_nacimiento"]
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()

    # Obtiene la fecha actual
    fecha_actual = datetime.now().date()

    # Compara la fecha de nacimiento con la fecha actual
    if fecha_nacimiento >= fecha_actual:
        flash("La fecha de nacimiento debe ser en el pasado.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento_str,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))
    
    # Obtén la fecha de nacimiento del formulario
    fecha_nacimiento_str = request.form["fecha_nacimiento"]
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()

    # Obtén la fecha de inicio del formulario
    fecha_inicio_str = request.form["fecha_inicio"]
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()

    # Obtiene la fecha actual
    fecha_actual = datetime.now().date()

    # Compara la fecha de nacimiento con la fecha de inicio
    if fecha_nacimiento >= fecha_inicio:
        flash("La fecha de nacimiento debe ser anterior a la fecha de inicio.", "error")
        session['form_data'] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento_str,
            'fecha_inicio': fecha_inicio_str,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,
            'dia': dia,
            'horario': horario,
            'materia': materia
        }
        return redirect(url_for('alta'))

    if nombre and apellido and email and telefono and fecha_nacimiento and fecha_inicio and colegio and curso and nivel_educativo and nombre_titular and telefono_titular and dia and horario and materia:
        cursor = db.database.cursor()
        sql = "UPDATE alumnos SET nombre = %s, apellido  = %s, email  = %s, telefono = %s, fecha_nacimiento = %s, fecha_inicio = %s, colegio = %s, curso = %s, nivel_educativo = %s, nombre_titular = %s, telefono_titular = %s, dia = %s, horario = %s, materia = %s WHERE id = %s"
        data = (nombre, apellido, email, telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular, dia, horario, materia, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('alta'))


# Ingresos

@app.route("/ingresos", methods=["GET", "POST"])
def ingresos():
    form_data = session.pop('form_data', None)  # Obtener los datos del formulario almacenados en sesión
    
    # Define las variables con valores predeterminados (pueden ser None u otros valores apropiados)
    fecha_pago = None
    fecha_actual = None
    nombre_alumno = None
    apellido_alumno = None
    monto = None
    medios_de_pago = None
    
    if request.method == "POST":
        # Obtén la fecha de pago del formulario
        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()

        # Mueve la obtención del nombre_alumno aquí
        nombre_alumno = request.form["nombre_alumno"]

        # Verifica si ya existe un pago para el mismo alumno en el mismo mes y año
        cursor = db.database.cursor()
        cursor.execute("SELECT COUNT(*) FROM ingresos WHERE nombre_alumno = %s AND MONTH(fecha_pago) = %s AND YEAR(fecha_pago) = %s", (nombre_alumno, fecha_pago.month, fecha_pago.year))
        pago_existente = cursor.fetchone()[0]
        cursor.close()

        if pago_existente > 0:
            flash("Ya existe un pago para este alumno en el mismo mes y año.", "error")
            session['form_data'] = {
                'nombre_alumno': nombre_alumno,
                'fecha_pago': fecha_pago_str,
                'monto': monto,
                'medios_de_pago': medios_de_pago
            }
            return redirect(url_for('ingresos'))

    if request.method == "POST":
        # Tu lógica para agregar datos aquí
        monto = request.form["monto"]
        medios_de_pago = request.form["medios_de_pago"]
        
       
        
        # Obtén la fecha de pago del formulario
        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()
        
        # Obtiene la fecha actual
        fecha_actual = datetime.now().date()
        
        if fecha_pago is not None and fecha_actual is not None and fecha_pago > fecha_actual:
            flash("La fecha de pago debe ser actual o anterior.", "error")
            session['form_data'] = {
                'nombre_alumno': nombre_alumno,
           
                'fecha_pago': fecha_pago_str,
                'monto': monto,
                'medios_de_pago': medios_de_pago
            }
            return redirect(url_for('ingresos'))
        
        if nombre_alumno and fecha_pago and monto and medios_de_pago:
            monto = monto.replace('$', '').replace(',', '')  # Elimina "$" y comas
            monto = float(monto)  
        # Remove the existing SQL statement
            cursor = db.database.cursor()
            sql = "INSERT INTO ingresos (nombre_alumno, fecha_pago, monto, medios_de_pago) VALUES (%s, %s, %s, %s)"
            data = (nombre_alumno, fecha_pago, monto, medios_de_pago)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
            return redirect(url_for('ingresos'))

            
        
    
    # Tu lógica para mostrar la página de ingresos con la lista de datos aquí
    cursor = db.database.cursor()
    cursor.execute("SELECT id_ingresos, nombre_alumno,  fecha_pago, monto, medios_de_pago FROM ingresos")
    myresult = cursor.fetchall()
    
    # Convertir los datos a un diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    
    cursor.close()
    # Obtener la lista de nombres y apellidos de los alumnos
    # Tu lógica para mostrar la página de ingresos con la lista de datos aquí
    cursor = db.database.cursor()
    cursor.execute("SELECT id_ingresos, nombre_alumno, apellido_alumno, fecha_pago, monto, medios_de_pago FROM ingresos")
    myresult = cursor.fetchall()

    # Obtener la lista de nombres y apellidos de los alumnos
    cursor.execute("SELECT nombre, apellido FROM alumnos")
    alumnos = cursor.fetchall()
    cursor.close()

    # Crear una lista de nombres y apellidos concatenados
    nombres_apellidos = [f"{alumno[0]} {alumno[1]}" for alumno in alumnos]

    return render_template("ingresos.html", data=insertObject, form_data=form_data, nombres_apellidos=nombres_apellidos)





#Eliminar
@app.route("/eliminar_ingresos/<string:id_ingresos>")
def eliminar_ingresos(id_ingresos):
    cursor = db.database.cursor()
    sql =  "DELETE FROM ingresos WHERE id_ingresos = %s"
    data = (id_ingresos,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('ingresos'))


# Actualizar ingresos
@app.route("/editaringresos/<int:id_ingresos>", methods=["POST", "GET"])
def editaringresos(id_ingresos):
    registro_editar = None  # Define registro_editar inicialmente como None

    if request.method == "GET":
        cursor = db.database.cursor()
        cursor.execute("SELECT nombre_alumno,fecha_pago, monto, medios_de_pago FROM ingresos WHERE id_ingresos = %s", (id_ingresos,))
        registro_editar = cursor.fetchone()
        cursor.close()
        data = db.database
        if registro_editar:
            return render_template("editar_ingresos.html", registro=registro_editar, data=data)
        else:
            # Manejar el caso si no se encuentra el registro a editar
            flash("Registro no encontrado.", "error")
            return redirect(url_for('ingresos'))

    if request.method == "POST":
        nombre_alumno = request.form["nombre_alumno"]

        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()
        monto = request.form["monto"]
        medios_de_pago = request.form["medios_de_pago"]

       

        # Obtiene la fecha actual
        fecha_actual = datetime.now().date()

        # Compara la fecha de pago con la fecha actual
        if fecha_pago is not None and fecha_actual is not None and fecha_pago > fecha_actual:
            flash("La fecha de pago debe ser actual o anterior.", "error")
            session['form_data'] = {
                'nombre_alumno': nombre_alumno,
           
                'fecha_pago': fecha_pago_str,
                'monto': monto,
                'medios_de_pago': medios_de_pago
            }
            return redirect(url_for('editaringresos', id_ingresos=id_ingresos))

        if nombre_alumno and fecha_pago and monto and medios_de_pago:
            cursor = db.database.cursor()
            sql = "UPDATE ingresos SET nombre_alumno = %s,  fecha_pago = %s, monto = %s, medios_de_pago = %s WHERE id_ingresos = %s"
            data = (nombre_alumno, fecha_pago, monto, medios_de_pago, id_ingresos)
            cursor.execute(sql, data)
            db.database.commit()
            data = db.database
        return redirect(url_for('ingresos'))



#egresos
@app.route("/egresos", methods=["GET", "POST"])
def egresos():
    form_data = session.pop('form_data', None)  # Obtener los datos del formulario almacenados en sesión
    fecha_pago = None
    fecha_actual = None
    servicios= None
    monto= None
    medios_de_pago = None
    if request.method == "POST":
        # Tu lógica para agregar datos aquí
        servicios = request.form["servicios"]
        fecha_pago = request.form["fecha_pago"]
        monto = request.form["monto"]
        medios_de_pago = request.form["medios_de_pago"]
        
         # Obtén la fecha de pago del formulario
        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()
        
         # Obtiene la fecha actual
        fecha_actual = datetime.now().date()

    # Compara la fecha de pago con la fecha actual
    if fecha_pago is not None and fecha_actual is not None and fecha_pago > fecha_actual:
        flash("La fecha de pago debe ser actual o anterior.", "error")
        session['form_data'] = {
        'servicios': servicios,
        'fecha_pago': fecha_pago_str,
        'monto':monto,
        'medios_de_pago':medios_de_pago
        }
        return redirect(url_for('egresos'))

    if servicios and fecha_pago and monto and medios_de_pago:
        monto = monto.replace('$', '').replace(',', '')  # Elimina "$" y comas
        monto = float(monto)  
        cursor = db.database.cursor()
        sql = "INSERT INTO egresos (servicios, fecha_pago, monto, medios_de_pago) VALUES (%s, %s, %s, %s)"
        data = (servicios, fecha_pago, monto, medios_de_pago)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('egresos'))  # Redirige a la misma vista después de agregar datos

# Tu lógica para mostrar la página de egresos con la lista de datos aquí
    cursor = db.database.cursor()
    cursor.execute("SELECT id, servicios, fecha_pago, monto, medios_de_pago FROM egresos")
    myresult = cursor.fetchall()
    # Convertirmos los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    data=db.database
    return render_template("egresos.html", data=insertObject,form_data=form_data)



#Eliminar
@app.route("/eliminar_egresos/<string:id>")
def eliminar_egresos(id):
    cursor = db.database.cursor()
    sql =  "DELETE FROM egresos WHERE id = %s"
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('egresos'))


#Actualizar
@app.route("/editaregresos/<int:id>", methods=["POST", "GET"])
def editaregresos(id):
    registro_editar = None  # Define registro_editar inicialmente como None

    if request.method == "GET":
        cursor = db.database.cursor()
        cursor.execute("SELECT servicios, fecha_pago, monto, medios_de_pago FROM egresos WHERE id = %s", (id,))
        registro_editar = cursor.fetchone()
        cursor.close()
        data=db.database

        if registro_editar:
            return render_template("editar_egresos.html", registro=registro_editar,data=data)
        else:
            # Manejar el caso si no se encuentra el registro a editar
            flash("Registro no encontrado.", "error")
            return redirect(url_for('egresos'))

    if request.method == "POST":
        servicios = request.form["servicios"]
        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()
        monto = request.form["monto"]
        medios_de_pago = request.form["medios_de_pago"]

        # Obtiene la fecha actual
        fecha_actual = datetime.now().date()

    # Compara la fecha de pago con la fecha actual
    if fecha_pago is not None and fecha_actual is not None and fecha_pago > fecha_actual:
        flash("La fecha de pago debe ser actual o anterior.", "error")
        session['form_data'] = {
        'servicios': servicios,
        'fecha_pago': fecha_pago_str,
        'monto':monto,
        'medios_de_pago':medios_de_pago
        }
        return redirect(url_for('egresos'))
    if servicios and fecha_pago and monto and medios_de_pago:
            cursor = db.database.cursor()
            sql = "UPDATE egresos SET servicios = %s, fecha_pago = %s, monto = %s, medios_de_pago = %s WHERE id = %s"
            data = (servicios, fecha_pago, monto, medios_de_pago, id)
            cursor.execute(sql, data)
            db.database.commit()
            data=db.database
    return redirect(url_for('egresos'))

#Caja
@app.route('/caja')
def caja():
    return render_template('resumen.html')

#Agenda
@app.route('/agenda')
def agenda():
    return render_template('agenda.html')

#Agenda
@app.route('/control')
def control():
    return render_template('control.html')

#PDF de ingresos

@app.route('/descargar_pdf/<int:id_ingresos>')
def descargar_pdf(id_ingresos):
    # Obtén los datos del alumno con el ID proporcionado 
    cursor = db.database.cursor()
    cursor.execute("SELECT nombre_alumno,fecha_pago, monto, medios_de_pago FROM ingresos WHERE id_ingresos = %s", (id_ingresos,))
    alumno = cursor.fetchone()
    cursor.close()

    if alumno is None:
        return "Alumno no encontrado", 404

    # Genera el PDF con los datos del alumno
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

      # Agrega la imagen en la parte superior izquierda (ajusta las coordenadas según tu diseño)
    c.drawImage("src/static/img/logo_fondo_1.png", 40, 690, width=120, height=100)

    # Agrega una línea que ocupe todo el ancho (ajusta las coordenadas según tu diseño)
    c.line(50, 670, 550, 670)

    # Agrega el título (ajusta las coordenadas y el estilo según tu diseño)
    c.setFont("Helvetica", 16)
    c.drawString(220, 700, "Recibo de Pago")

    # Agrega el texto debajo del título (ajusta las coordenadas y el estilo según tu diseño)
    c.setFont("Helvetica", 12)
    texto_recibo = f"El recibo corresponde a {alumno[0]} por el monto de ${alumno[2]} en la fecha {alumno[1]}."
    c.drawString(50, 610, texto_recibo)
    
    c.drawString(230, 130, "Firma del receptor: __________________________")


    c.save()

    pdf_buffer.seek(0)

    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={alumno[0]}_{alumno[1]}.pdf'
    
    return response




app.secret_key = 'veronica'
if __name__ == "__main__":
    app.run(debug =  True, port = 4000)