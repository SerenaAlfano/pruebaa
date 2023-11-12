import mysql.connector
import os #Permite acceder a los directorios
import re
import json

from flask import Flask, render_template, request, redirect, url_for, flash, session,  jsonify, send_from_directory
from datetime import datetime
from flask_mysqldb import MySQL
from datetime import timedelta
from datetime import datetime

from flask_login import LoginManager,logout_user, login_user
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors 
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from flask import make_response
from reportlab.lib.styles import getSampleStyleSheet
from config import config
from datetime import timedelta

# Función para convertir timedelta a un formato serializable
def convert_timedelta_to_str(td):
    total_seconds = td.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,"src", "templates")

app = Flask(__name__, template_folder = template_dir)

db = MySQL(app)
db_config = config["development"]

#Conexión a la base de datos
db_connection = mysql.connector.connect(
    host=db_config.MYSQL_HOST,
    user=db_config.MYSQL_USER,
    password=db_config.MYSQL_PASSWORD,
    database=db_config.MYSQL_DB
)

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

#Validaciones
#Verifica que el nombre contiene solo letras y espacios
def validar_nombre(nombre):
    return bool(re.match(r'^[a-zA-Z\s]+$', nombre))
#Verifica que el apellido contiene solo letras y espacios
def validar_apellido(apellido):
    return bool(re.match(r'^[a-zA-Z\s]+$', apellido))
#Verifica que el nombre contiene solo letras y espacios
def validar_nombre_titular(nombre_titular):
    return bool(re.match(r'^[a-zA-Z\s]+$', nombre_titular))
#Verifica que el nombre contiene solo letras y espacios
def validar_nombre_alumno(nombre_alumno):
    return bool(re.match(r'^[a-zA-Z\s]+$', nombre_alumno))
#Verifica que el apellido contiene solo letras y espacios
def validar_apellido_alumno(apellido_alumno):
    return bool(re.match(r'^[a-zA-Z\s]+$', apellido_alumno))

#Verifica que el teléfono contiene solo números y ciertos carácteres especiales como +, -, (, y )
def validar_telefono(telefono):
    patron = r"^[0-9+\-() ]+$"
    if re.match(patron, telefono):
        return True
    else:
        return False 
#Verifica que el número de teléfono contiene solo números y ciertos caracteres especiales como +, -, (, y )    
def validar_telefono_titular(telefono_titular):   
    patron = r"^[0-9+\-() ]+$"
    
    if re.match(patron, telefono_titular):
        return True
    else:
        return False 
    
def validar_dni(dni):
    # Utilizamos una expresión regular para verificar que el DNI cumpla con los requisitos
    patron = r'^\d{1,8}$'  # Acepta de 1 a 8 dígitos

    if re.match(patron, dni):
        return True
    else:
        return False

    
#RUTAS

@app.route('/')
def index():
    return redirect(url_for('login'))

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('inicio'))
            else:
                flash("Contraseña inválida")
                return render_template('auth/login.html')
        else:
            flash("Usuario incorrecto")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

#Logout
@app.route('/logout')
def logout():
    logout_user()
    return render_template('auth/login.html')

#Home
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

#Nuevo alumno
@app.route("/index")
def alta():
    form_data = session.pop('form_data', None)  # Obtener los datos del formulario almacenados en sesión
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM alumnos")
    myresult = cursor.fetchall()
    # Consulta para recuperar la lista de cursos,nivel educativo,dia y materias desde la base de datos "matricula"
    cursor.execute("SELECT nombre FROM matricula.curso")
    cursos = [curso[0] for curso in cursor.fetchall()]
    cursor.execute("SELECT  nombre_nivel FROM nivel_educativo")
    niveles_educativos = [row[0] for row in cursor.fetchall()]
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("index.html", data=insertObject, form_data=form_data, cursos=cursos, niveles_educativos=niveles_educativos)

@app.route("/agregarAlumno", methods=["POST", "GET"])
def agregarAlumno():  
    cursor = db_connection.cursor()
    dni = request.form["dni"]
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

   

     # Consulta SQL para verificar si el DNI ya existe en la tabla de alumnos
    check_query = "SELECT COUNT(*) FROM alumnos WHERE dni = %s"
    check_data = (dni,)
    cursor.execute(check_query, check_data)
    result = cursor.fetchone()
    if result[0] > 0:
        flash("El alumno ya se encuentra registrado en el sistema.", "error")
        return redirect(url_for('alta'))  # Redirige de vuelta al formulario de alta
    
    if validar_dni(dni):
        print("El DNI es válido.")
    else:
        flash("El DNI no es válido. Debe contener solo números y tener como máximo 8 dígitos.", "error")
        session['form_data'] = {
        'dni': dni,
        'apellido': apellido,
        'nombre': nombre,
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,        
        }
        return redirect(url_for('alta'))


    if not validar_nombre(nombre):
        flash("El nombre no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'dni' : dni,
            'apellido': apellido,
            'nombre': nombre, 
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,          
        }
        return redirect(url_for('alta'))
    
    if not validar_telefono(telefono):
        flash("El número de teléfono no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
        'dni' : dni,
        'apellido': apellido,
        'nombre': nombre, 
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,       
        }
        return redirect(url_for('alta'))

    if not validar_apellido(apellido):
        flash("El apellido no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'dni' : dni, 
            'apellido': apellido,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,        
        }
        return redirect(url_for('alta'))

    if not validar_nombre_titular(nombre_titular):
        flash("El nombre del tutor no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'dni' : dni,
            'apellido': apellido,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,     
        }
        return redirect(url_for('alta'))
    
    if not validar_telefono_titular(telefono_titular):
        flash("El número de teléfono tutor no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
        'dni' : dni,
        'apellido': apellido,
        'nombre': nombre,      
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,
        }
        return redirect(url_for('alta'))

    # Obtiene la fecha de nacimiento del formulario
    fecha_nacimiento_str = request.form["fecha_nacimiento"]
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
    # Obtiene la fecha actual
    fecha_actual = datetime.now().date()

    # Compara la fecha de nacimiento con la fecha actual
    if fecha_nacimiento >= fecha_actual:
        flash("La fecha de nacimiento debe ser en el pasado.", "error")
        session['form_data'] = {
            'dni' : dni,
            'apellido': apellido,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento_str,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,           
        }
        return redirect(url_for('alta'))
    
    # Calcula la fecha mínima permitida para la fecha de nacimiento (6 años atrás)
    fecha_minima = fecha_actual - timedelta(days=365 * 6)

    # Compara la fecha de nacimiento con la fecha mínima
    if fecha_nacimiento > fecha_minima:
        flash("El alumno debe tener al menos 6 años de edad.", "error")
        session['form_data'] = {
            'dni' : dni,
            'apellido': apellido,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento_str,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,         
        }
        return redirect(url_for('alta'))
    email = request.form["email"]
    if any(letra.isupper() for letra in email):
        flash("El campo de correo electrónico no debe contener letras mayúsculas.", "error")
        session['form_data'] = {
        'dni' : dni,
        'apellido': apellido,
        'nombre': nombre, 
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,      
    }
        return redirect(url_for('alta'))
        
  

    # Si el conteo es menor a 4, procedemos a insertar el nuevo alumno
    insert_query = "INSERT INTO alumnos (dni,apellido,nombre, email, telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (dni,apellido, nombre,  email ,telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular)
    try:
        cursor.execute(insert_query, data)
        db_connection.commit() 
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}") 
    return redirect(url_for('listado'))


#Listado de alumnos
@app.route("/listado")
def listado():
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM alumnos ORDER BY apellido ASC;")
    myresult = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("listado.html", data=insertObject)


@app.route("/eliminar/<string:id>")
def eliminar(id):
    try:
        cursor = db_connection.cursor()
        sql = "DELETE FROM alumnos WHERE id = %s"
        data = (id,)
        cursor.execute(sql, data)
        db_connection.commit()
        return jsonify({"success": True, "data": None})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Actualizar
@app.route("/editar/<string:id>", methods=["POST"])
def editar(id):
    cursor = db_connection.cursor()
    dni = request.form["dni"]
    apellido = request.form["apellido"]
    nombre = request.form["nombre"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    fecha_inicio = request.form["fecha_inicio"]
    colegio = request.form["colegio"]
    curso = request.form["curso"]
    nivel_educativo = request.form["nivel_educativo"]
    nombre_titular = request.form["nombre_titular"]
    telefono_titular = request.form["telefono_titular"]

    if validar_dni(dni):
        print("El DNI es válido.")
    else:
        flash("El DNI no es válido. Debe contener solo números y tener como máximo 8 dígitos.", "error")
        session['form_data'] = {
            'dni': dni,
            'apellido': apellido,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,   
            }
        return redirect(url_for('listado'))
    
    if not validar_nombre_titular(nombre_titular):
        flash("El nombre del tutor no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'dni': dni,
            'apellido': apellido,
            'nombre': nombre,           
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,          
        }
        return redirect(url_for('listado'))
    
    if not validar_telefono(telefono):
        flash("El número de teléfono no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
        'dni': dni,
        'apellido': apellido,
        'nombre': nombre,   
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,      
        }
        return redirect(url_for('listado'))
    
    if not validar_telefono_titular(telefono_titular):
        flash("El número de teléfono del tutor no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
    }
        return redirect(url_for('listado'))

    if not validar_telefono(telefono):
        flash("El número de teléfono no es válido. Debe contener solo dígitos.", "error")
        session['form_data'] = {
        'dni': dni,
        'apellido': apellido,
        'nombre': nombre,
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,       
        }
        return redirect(url_for('listado'))

    if not validar_nombre(nombre):
        flash("El nombre no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'dni': dni,
            'apellido': apellido,
            'nombre': nombre, 
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,          
        }
        return redirect(url_for('listado'))

    if not validar_apellido(apellido):
        flash("El apellido no es válido. Debe contener solo letras.", "error")
        session['form_data'] = {
            'dni': dni,
            'apellido': apellido,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,           
        }
        return redirect(url_for('listado'))
    
    email = request.form["email"]
    if any(letra.isupper() for letra in email):
        flash("El campo de correo electrónico no debe contener letras mayúsculas.", "error")
        session['form_data'] = {
        'dni': dni,
        'apellido': apellido,
        'nombre': nombre,       
        'email': email,
        'telefono': telefono,
        'fecha_nacimiento': fecha_nacimiento,
        'fecha_inicio': fecha_inicio,
        'colegio': colegio,
        'curso': curso,
        'nivel_educativo': nivel_educativo,
        'nombre_titular': nombre_titular,
        'telefono_titular': telefono_titular,      
    }
        return redirect(url_for('listado'))
    
    # Obtiene la fecha de nacimiento del formulario
    fecha_nacimiento_str = request.form["fecha_nacimiento"]
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()

    # Obtiene la fecha actual
    fecha_actual = datetime.now().date()

    # Compara la fecha de nacimiento con la fecha actual
    if fecha_nacimiento >= fecha_actual:
        flash("La fecha de nacimiento debe ser en el pasado.", "error")
        session['form_data'] = {
            'dni': dni,
            'apellido': apellido,
            'nombre': nombre,    
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento_str,
            'fecha_inicio': fecha_inicio,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,           
        }
        return redirect(url_for('listado'))
    
    # Obtiene la fecha de nacimiento del formulario
    fecha_nacimiento_str = request.form["fecha_nacimiento"]
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()

    # Obtiene la fecha de inicio del formulario
    fecha_inicio_str = request.form["fecha_inicio"]
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()

    # Obtiene la fecha actual
    fecha_actual = datetime.now().date()

    # Compara la fecha de nacimiento con la fecha de inicio
    if fecha_nacimiento >= fecha_inicio:
        flash("La fecha de nacimiento debe ser anterior a la fecha de inicio.", "error")
        session['form_data'] = {
            'dni': dni,
            'apellido': apellido,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'fecha_nacimiento': fecha_nacimiento_str,
            'fecha_inicio': fecha_inicio_str,
            'colegio': colegio,
            'curso': curso,
            'nivel_educativo': nivel_educativo,
            'nombre_titular': nombre_titular,
            'telefono_titular': telefono_titular,           
        }
        return redirect(url_for('listado'))
    

    try:
  
        result = cursor.fetchone()
        if result[0] >= 4:
            flash("Ya hay 4 alumnos registrados en este horario.", "error")
            session['form_data'] = {
                'dni': dni,
                'apellido': apellido,
                'nombre': nombre,               
                'email': email,
                'telefono': telefono,
                'fecha_nacimiento': fecha_nacimiento_str,
                'fecha_inicio': fecha_inicio_str,
                'colegio': colegio,
                'curso': curso,
                'nivel_educativo': nivel_educativo,
                'nombre_titular': nombre_titular,
                'telefono_titular': telefono_titular,             
            }
            return redirect(url_for('listado'))

    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")

    # Continúa con la actualización de la base de datos
    if dni and apellido and nombre and email and telefono and fecha_nacimiento and fecha_inicio and colegio and curso and nivel_educativo and nombre_titular and telefono_titular:
        cursor = db_connection.cursor()
        data = (dni, apellido,nombre,  email, telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular, id)
        sql = "UPDATE alumnos SET dni = %s, apellido = %s, nombre = %s, email = %s, telefono = %s, fecha_nacimiento = %s, fecha_inicio = %s, colegio = %s, curso = %s, nivel_educativo = %s, nombre_titular = %s, telefono_titular = %s WHERE id = %s"


        try:
            cursor.execute(sql, data)
            db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error de MySQL: {err}")
            flash("Error al actualizar el alumno en la base de datos.", "error")

    return redirect(url_for('listado'))


# Ingresos
@app.route("/ingresos", methods=["GET", "POST"])
def ingresos():
    cursor = db_connection.cursor()  # Inicializa cursor
    cursor.execute("SELECT nombre_medio_pago FROM medios_pago")
    medios_pago_disponibles = [medio_pago[0] for medio_pago in cursor.fetchall()]

    cursor.execute("SELECT nombre_tipo_pago FROM tipos_pago")
    tipos_pago_disponibles = [tipo_pago[0] for tipo_pago in cursor.fetchall()]
    form_data = session.pop('form_data', None)  # Obtiene los datos del formulario almacenados en sesión
    
    # Define las variables con valores predeterminados (pueden ser None u otros valores apropiados)
    fecha_pago = None
    fecha_actual = None
    nombre_alumno = None
    monto = None
    medios_de_pago = None
    tipo_pago = None
    
    if request.method == "POST":
        # Obtiene la fecha de pago del formulario
        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()
        # Mueve la obtención del nombre_alumno
        nombre_alumno = request.form["nombre_alumno"]
        # Verifica si ya existe un pago para el mismo alumno en el mismo mes y año
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM ingresos WHERE nombre_alumno = %s AND MONTH(fecha_pago) = %s AND YEAR(fecha_pago) = %s", (nombre_alumno, fecha_pago.month, fecha_pago.year))
        pago_existente = cursor.fetchone()[0]
        cursor.close()

        if pago_existente > 0:
            flash("Ya existe un pago para este alumno en el mismo mes y año.", "error")
            session['form_data'] = {
                'nombre_alumno': nombre_alumno,
                'fecha_pago': fecha_pago_str,
                'monto': monto,
                'medios_de_pago': medios_de_pago,
                'tipo_pago': tipo_pago
            }
            return redirect(url_for('ingresos'))

    if request.method == "POST":
        monto = request.form["monto"]
        medios_de_pago = request.form["medios_de_pago"]
        tipo_pago = request.form["tipo_pago"]               
        # Obtiene la fecha de pago del formulario
        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()        
        # Obtiene la fecha actual
        fecha_actual = datetime.now().date()       
        if fecha_pago > fecha_actual:
            flash("La fecha de pago debe ser actual o anterior.", "error")
            session['form_data'] = {
                'nombre_alumno': nombre_alumno,
                'fecha_pago': fecha_pago_str,
                'monto': monto,
                'medios_de_pago': medios_de_pago,
                'tipo_pago': tipo_pago
            }
            return redirect(url_for('ingresos'))
        
        if nombre_alumno and fecha_pago and monto and medios_de_pago:
            monto = monto.replace('$', '').replace(',', '')  # Elimina "$" y comas
            monto = float(monto) 
            cursor = db_connection.cursor()
            sql = "INSERT INTO ingresos (nombre_alumno, fecha_pago, monto, medios_de_pago,tipo_pago) VALUES (%s, %s, %s, %s, %s)"
            data = (nombre_alumno, fecha_pago, monto, medios_de_pago,tipo_pago)
            cursor.execute(sql, data)
            db_connection.commit()
            cursor.close()
            return redirect(url_for('ingresos'))
    
    
    #Muestra la página de ingresos con la lista de datos
    cursor = db_connection.cursor()
    cursor.execute("SELECT id_ingresos, nombre_alumno,  fecha_pago, monto, medios_de_pago, tipo_pago FROM ingresos")
    myresult = cursor.fetchall()
    
    #Convierte los datos a un diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    #Obtiene la lista de nombres y apellidos de los alumnos
    #Muestra la página de ingresos con la lista de datos 
    cursor = db_connection.cursor()
    cursor.execute("SELECT id_ingresos, nombre_alumno, apellido_alumno, fecha_pago, monto, medios_de_pago, tipo_pago FROM ingresos")
    myresult = cursor.fetchall()
    # Obtiene la lista de nombres y apellidos de los alumnos
    cursor.execute("SELECT nombre, apellido FROM alumnos")
    alumnos = cursor.fetchall()
    cursor.close()
    # Crea una lista de nombres y apellidos concatenados
    nombres_apellidos = [f"{alumno[0]} {alumno[1]}" for alumno in alumnos]
    return render_template("ingresos.html", data=insertObject, form_data=form_data, nombres_apellidos=nombres_apellidos, medios_pago_disponibles=medios_pago_disponibles)

#Eliminar Ingresos
@app.route("/eliminar_ingresos/<string:id_ingresos>")
def eliminar_ingresos(id_ingresos):
    cursor = db_connection.cursor()
    try:
        sql = "DELETE FROM ingresos WHERE id_ingresos = %s"
        data = (id_ingresos,)
        cursor.execute(sql, data)
        db_connection.commit()
        return jsonify({"success": True})
    except Exception as e:
        db_connection.rollback()
        return jsonify({"success": False, "error_message": str(e)})


# Actualizar ingresos
def obtener_medios_pago():
    cursor = db_connection.cursor()
    cursor.execute("SELECT nombre_medio_pago FROM medios_pago")
    medios_pago = [medio_pago[0] for medio_pago in cursor.fetchall()]
    cursor.close()
    return medios_pago

def obtener_tipos_pago():
    cursor = db_connection.cursor()
    cursor.execute("SELECT nombre_tipo_pago FROM tipos_pago")
    tipos_pago = [tipo_pago[0] for tipo_pago in cursor.fetchall()]
    cursor.close()
    return tipos_pago



@app.route("/editaringresos/<int:id_ingresos>", methods=["POST", "GET"])

def editaringresos(id_ingresos):
    registro_editar = None  # Define registro_editar inicialmente como None
    
    if request.method == "GET":
        cursor = db.database.cursor()
        cursor.execute("SELECT nombre_alumno,fecha_pago, monto, medios_de_pago, tipo_pago FROM ingresos WHERE id_ingresos = %s", (id_ingresos,))
        registro_editar = cursor.fetchone()
        medios_pago_query = "SELECT nombre FROM medios_pago"
        cursor.execute(medios_pago_query)
        medios_pago = [row[0] for row in cursor.fetchall()]

        # Obtener opciones de tipos de pago desde la base de datos
        tipos_pago_query = "SELECT nombre FROM tipos_pago"
        cursor.execute(tipos_pago_query)
        tipos_pago = [row[0] for row in cursor.fetchall()]

        cursor.close()
        data = db.database
        # Obtiene el valor del monto sin formato desde la base de datos
        monto = registro_editar["monto"]
        # Formatea el monto como una cadena con el signo de peso, comas y punto
        monto_formateado = "${:,.2f}".format(monto)
        medios_pago = obtener_medios_pago()  # Obtener las opciones de medios de pago
        tipos_pago = obtener_tipos_pago() 
        return render_template("editar_ingresos.html", monto_formateado=monto_formateado, registro=registro_editar, data=data, medios_pago=medios_pago, tipos_pago=tipos_pago)

    if request.method == "POST":
        nombre_alumno = request.form["nombre_alumno"]
        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()
        monto = request.form["monto"]
        medios_de_pago = request.form["medios_de_pago"]
        tipo_pago = request.form["tipo_pago"]
        # Obtiene la fecha actual
        fecha_actual = datetime.now().date()
        # Compara la fecha de pago con la fecha actual
        if fecha_pago is not None and fecha_actual is not None and fecha_pago > fecha_actual:
            flash("La fecha de pago debe ser actual o anterior.", "error")
            session['form_data'] = {
                'nombre_alumno': nombre_alumno,
                'fecha_pago': fecha_pago_str,
                'monto': monto,
                ' tipo_pago':  tipo_pago

            }
            return redirect(url_for('editaringresos', id_ingresos=id_ingresos))
        if nombre_alumno and fecha_pago and monto and medios_de_pago:
            cursor = db_connection.cursor()
            sql = "UPDATE ingresos SET nombre_alumno = %s,  fecha_pago = %s, monto = %s, medios_de_pago = %s ,  tipo_pago = %s WHERE id_ingresos = %s"
            data = (nombre_alumno, fecha_pago, monto, medios_de_pago, tipo_pago, id_ingresos)
            

            cursor.execute(sql, data)
            db_connection.commit()
            # Realiza una consulta para obtener los datos actualizados
            cursor.execute("SELECT * FROM ingresos WHERE id_ingresos = %s", (id_ingresos,))
            updated_data = cursor.fetchone()  # Obtiene la fila actualizada
            cursor.close()  # Cierra el cursor
            
        return redirect(url_for('ingresos'))

#Egresos
@app.route("/egresos", methods=["GET", "POST"])
def egresos():
    form_data = session.pop('form_data', None)  # Obtiene los datos del formulario almacenados en sesión
    servicios= None
    fecha_pago = None
    fecha_actual = None 
    monto= None
    medios_de_pago = None
    if request.method == "POST":
        servicios = request.form["servicios"]
        fecha_pago = request.form["fecha_pago"]
        monto = request.form["monto"]
        medios_de_pago = request.form["medios_de_pago"]

        cursor = db_connection.cursor()
        cursor.execute("SELECT id, nombre_medio_pago FROM medios_pago")
        medios_de_pago_rows = cursor.fetchall()
        cursor.close()

        #Verifica si el servicio es un gasto fijo mensual
        gastos_fijos_mensuales = ["luz", "agua", "gas", "internet"]
        if servicios.lower() in gastos_fijos_mensuales:
             #Verifica si el servicio ya se ha registrado este mes
             cursor = db_connection.cursor()
             cursor.execute("SELECT COUNT(*) FROM egresos WHERE servicios = %s AND MONTH(fecha_pago) = MONTH(CURRENT_DATE())", (servicios,))
             count = cursor.fetchone()[0]
             cursor.close()
             if count > 0:
                flash(f"El servicio {servicios} ya se ha registrado este mes.", "error")
                session['form_data'] = {
                    'servicios': servicios,
                    'fecha_pago': fecha_pago,
                    'monto': monto,
                    'medios_de_pago': medios_de_pago
                }
                return redirect(url_for('egresos'))
        
        #Obtiene la fecha de pago del formulario
        fecha_pago_str = request.form["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d").date()
        #Obtiene la fecha actual
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
        cursor = db_connection.cursor()
        sql = "INSERT INTO egresos (servicios, fecha_pago, monto, medios_de_pago) VALUES (%s, %s, %s, %s)"
        data = (servicios, fecha_pago, monto, medios_de_pago)       
        cursor.execute(sql, data)
        db_connection.commit()
        return redirect(url_for('egresos')) 

    cursor = db_connection.cursor()
    cursor.execute("SELECT id, servicios, fecha_pago, monto, medios_de_pago FROM egresos")
    myresult = cursor.fetchall()
    #Convierte los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()  
    return render_template("egresos.html", data=insertObject,form_data=form_data, medios_de_pago=medios_de_pago)

# Eliminar egresos
# Agrega una nueva ruta para eliminar egresos
@app.route("/eliminar_egresos/<string:id>")
def eliminar_egresos(id):
    try:
        cursor = db_connection.cursor()
        sql = "DELETE FROM egresos WHERE id = %s"
        data = (id,)
        cursor.execute(sql, data)
        db_connection.commit()
        return jsonify({"success": True})
    except mysql.connector.Error as err:
        print("Error MySQL al eliminar el egreso:", err)
        return jsonify({"success": False, "error_message": "Error al eliminar el egreso. Ocurrió un error durante la eliminación."})



#Actualizar egresos
@app.route("/editaregresos/<int:id>", methods=["POST", "GET"])
def editaregresos(id):
    registro_editar = None 
    if request.method == "GET":
        cursor = db_connection.cursor()
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
            cursor = db_connection.cursor()
            sql = "UPDATE egresos SET servicios = %s, fecha_pago = %s, monto = %s, medios_de_pago = %s WHERE id = %s"
            data = (servicios, fecha_pago, monto, medios_de_pago, id)
            cursor.execute(sql, data)
            db_connection.commit()

    return redirect(url_for('egresos'))

#Caja
@app.route('/caja', methods=['GET', 'POST'])
def caja():
    cursor = db_connection.cursor()

    #Consulta para obtener el total de ingresos
    cursor.execute("SELECT SUM(monto) FROM ingresos")
    total_ingresos = cursor.fetchone()[0]

    #Consulta para obtener el total de egresos
    cursor.execute("SELECT SUM(monto) FROM egresos")
    total_egresos = cursor.fetchone()[0]
    
    #Calcula el saldo restando los totales de egresos de los totales de ingresos
    saldo = total_egresos - total_ingresos  
    return render_template('caja.html',total_ingresos=total_ingresos, total_egresos=total_egresos, saldo=saldo)


#Agenda
@app.route("/agenda", methods=["GET", "POST"])
def agenda():
    return render_template("agenda.php")

#PDF de ingresos
@app.route('/descargar_pdf/<int:id_ingresos>')
def descargar_pdf(id_ingresos):
    # Obtiene los datos del alumno con el ID 
    cursor = db_connection.cursor()
    cursor.execute("SELECT nombre_alumno,fecha_pago, monto, medios_de_pago FROM ingresos WHERE id_ingresos = %s", (id_ingresos,))
    alumno = cursor.fetchone()
    cursor.close()

    if alumno is None:
        return "Alumno no encontrado", 404

    #Genera el PDF con los datos del alumno
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    #Agrega la imagen en la parte superior izquierda
    c.drawImage("src/static/img/logo_fondo_1.png", 40, 690, width=120, height=100)

    #Agrega una línea que ocupa todo el ancho 
    c.line(50, 670, 550, 670)

    #Agrega el título
    c.setFont("Helvetica", 16)
    c.drawString(220, 700, "Recibo de Pago")

    #Agrega el texto debajo del título 
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


#PDF para descargar el listado de alumnos
@app.route('/descargar_lista_alumnos_pdf')
def descargar_lista_alumnos_pdf():
    # Obtiene los datos de todos los alumnos en tu base de datos
    cursor = db_connection.cursor()
    cursor.execute("SELECT nombre, apellido, dni,  curso, nivel_educativo FROM alumnos")
    alumnos = cursor.fetchall()
    cursor.close()

    #Configura el búfer de bytes para el PDF
    pdf_buffer = BytesIO()

    #Crea un objeto SimpleDocTemplate para el PDF
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    #Crea una lista para almacenar los elementos del PDF
    elements = []

    #Agrega un título centrado al PDF
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title = Paragraph('<center><b>Listado de Alumnos</b></center>', title_style)
    elements.append(title)

    #Crea una lista para almacenar los datos de los alumnos
    data = [['Nombre', 'Apellido','DNI' ,'Curso', 'Nivel Educativo']]

    for alumno in alumnos:


        data.append([
            Paragraph(alumno[0], styles['Normal']),  # Nombre
            Paragraph(alumno[1], styles['Normal']),  # Apellido
            Paragraph(str(alumno[2]), styles['Normal']),  # DNI
            Paragraph(alumno[3], styles['Normal']),  # Curso
            Paragraph(alumno[4], styles['Normal']),  # Nivel Educativo
        ])

    # Crea una tabla para mostrar los datos de los alumnos
    table = Table(data)

    # Establece el estilo de la tabla para centrar el contenido
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centra verticalmente
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ])

    table.setStyle(style)

    # Agrega la tabla a la lista de elementos
    elements.append(table)

    # Construye el PDF
    doc.build(elements)

    # Configura las cabeceras adecuadas para la descarga
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=lista_alumnos.pdf'

    return response

# Definir la ruta para la descarga del PDF
@app.route('/descargar_pdf_manual', methods=['GET'])
def descargar_pdf_manual():
    directorio_pdf = r'C:\xampp\htdocs\prueba\pruebaa\src'
    nombre_pdf = 'manual_usuario.pdf'
    return send_from_directory(directorio_pdf, nombre_pdf)

# Ruta para renderizar la plantilla HTML que contiene el enlace para descargar el PDF
@app.route('/descargar_pdf', methods=['GET'])
def mostrar_pagina_descargar_pdf():
    return render_template('descargar_pdf.html')

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run(debug =  True, port = 4000)