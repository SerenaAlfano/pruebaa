from flask import Flask, render_template, request, redirect, url_for
import os #Permite acceder a los directorios
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,"src", "templates")

app = Flask(__name__, template_folder = template_dir)

#Rutas
@app.route("/")
def home(): 
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

    if nombre and apellido and email and telefono:
        cursor = db.database.cursor()
        sql =  "INSERT INTO alumnos (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)"
        data = (nombre, apellido, email, telefono)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))


#Eliminar
@app.route("/eliminar/<string:id>")
def eliminar(id):
    cursor = db.database.cursor()
    sql =  "DELETE FROM alumnos WHERE id = %s"
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home'))

#Actualizar
@app.route("/editar/<string:id>", methods = ["POST"])
def editar(id):
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    telefono = request.form["telefono"]

    if nombre and apellido and email and telefono:
        cursor = db.database.cursor()
        sql =  "UPDATE alumnos SET nombre = %s, apellido  = %s, email  = %s, telefono  = %s WHERE id = %s"
        data = (nombre, apellido, email, telefono, id)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug =  True, port = 4000)