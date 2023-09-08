from flask import Flask, render_template, request, redirect, url_for
import os #Permite acceder a los directorios
import database as db

from flask_wtf.csrf import CSRFProtect


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,"src", "templates")


app = Flask(__name__, template_folder = template_dir)

#Rutas
#Home
@app.route('/')
def inicio():
    
    return render_template('inicio.html')

@app.route("/index")
def alta(): 
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM alumnos")
    myresult = cursor.fetchall()
    #Convertirmos los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject .append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template("index.html", data = insertObject)

@app.route("/alumnos", methods=["POST"])
def agregarAlumno():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha_nacimiento= request.form["fecha_nacimiento"]
    fecha_inicio = request.form["fecha_inicio"]
    colegio = request.form["colegio"]
    curso = request.form["curso"]
    nivel_educativo = request.form["nivel_educativo"]
    nombre_titular = request.form["nombre_titular"]
    telefono_titular = request.form["telefono_titular"]
    dia = request.form["dia"]
    horario = request.form["horario"]
    materia = request.form["materia"]


    if nombre and apellido and email and telefono and fecha_nacimiento and fecha_inicio and colegio and curso and nivel_educativo and nombre_titular and telefono_titular and dia and horario and materia:
        cursor = db.database.cursor()
        sql =  "INSERT INTO alumnos (nombre, apellido, email, telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular, dia, horario, materia) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s)"
        data = (nombre, apellido, email, telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular, dia, horario, materia)
        cursor.execute(sql,data)
        db.database.commit()
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

#Actualizar
@app.route("/editar/<string:id>", methods = ["POST"])
def editar(id):
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha_nacimiento= request.form["fecha_nacimiento"]
    fecha_inicio = request.form["fecha_inicio"]
    colegio = request.form["colegio"]
    curso = request.form["curso"]
    nivel_educativo = request.form["nivel_educativo"]
    nombre_titular = request.form["nombre_titular"]
    telefono_titular = request.form["telefono_titular"]
    dia = request.form["dia"]
    horario = request.form["horario"]
    materia = request.form["materia"]

    if nombre and apellido and email and telefono and fecha_nacimiento and fecha_inicio and colegio and curso and nivel_educativo and nombre_titular and telefono_titular and dia and horario and materia:
        cursor = db.database.cursor()
        sql =  "UPDATE alumnos SET nombre = %s, apellido  = %s, email  = %s, telefono = %s, fecha_nacimiento = %s, fecha_inicio = %s, colegio = %s, curso = %s, nivel_educativo = %s, nombre_titular = %s, telefono_titular = %s, dia = %s, horario = %s, materia = %s WHERE id = %s"
        data = (nombre, apellido, email, telefono, fecha_nacimiento, fecha_inicio, colegio, curso, nivel_educativo, nombre_titular, telefono_titular, dia, horario, materia, id)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('alta'))


#Ingresos
#CargaDatos
@app.route("/ingresos", methods=["GET", "POST"])
def ingresos():
    if request.method == "POST":
        # Tu lógica para agregar datos aquí
        nombre_alumno = request.form["nombre_alumno"]
        apellido_alumno = request.form["apellido_alumno"]
        fecha_pago = request.form["fecha_pago"]
        monto = request.form["monto"]
        medios_de_pago = request.form["medios_de_pago"]

        if nombre_alumno and apellido_alumno and fecha_pago and monto and medios_de_pago:
            cursor = db.database.cursor()
            sql = "INSERT INTO ingresos (nombre_alumno, apellido_alumno, fecha_pago, monto, medios_de_pago) VALUES (%s, %s, %s, %s, %s)"
            data = (nombre_alumno, apellido_alumno, fecha_pago, monto, medios_de_pago)
            cursor.execute(sql, data)
            db.database.commit()

        return redirect(url_for('ingresos'))  # Redirige a la misma vista después de agregar datos


# Tu lógica para mostrar la página de ingresos con la lista de datos aquí
    cursor = db.database.cursor()
    cursor.execute("SELECT id_ingresos, nombre_alumno, apellido_alumno, fecha_pago, monto, medios_de_pago FROM ingresos")
    myresult = cursor.fetchall()
    # Convertirmos los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    
    return render_template("ingresos.html", data=insertObject)



#Eliminar
@app.route("/eliminar_ingresos/<string:id_ingresos>")
def eliminar_ingresos(id_ingresos):
    cursor = db.database.cursor()
    sql =  "DELETE FROM ingresos WHERE id_ingresos = %s"
    data = (id_ingresos,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('ingresos'))


#Actualizar
@app.route("/editaringresos/<int:id_ingresos>", methods = ["POST"])
def editaringresos(id_ingresos):
    nombre_alumno = request.form["nombre_alumno"]
    apellido_alumno = request.form["apellido_alumno"]
    fecha_pago = request.form["fecha_pago"]
    monto = request.form["monto"]
    medios_de_pago = request.form["medios_de_pago"]

    if nombre_alumno and apellido_alumno and fecha_pago and monto and medios_de_pago:
            cursor = db.database.cursor()
            sql = "UPDATE ingresos SET nombre_alumno = %s, apellido_alumno = %s, fecha_pago = %s, monto = %s, medios_de_pago = %s WHERE id_ingresos = %s"
            data = (nombre_alumno, apellido_alumno, fecha_pago, monto, medios_de_pago, id_ingresos)
            cursor.execute(sql, data)
            db.database.commit()

    return redirect(url_for('ingresos'))



#egresos
@app.route('/egresos')
def egresos():
    
    return render_template('egresos.html')

app.secret_key = 'veronica'
if __name__ == "__main__":
    app.run(debug =  True, port = 4000)