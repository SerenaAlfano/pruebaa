   dia = request.form.getlist("dia[]")
    horario = request.form["horario"]
    materia = request.form.getlist("materia[]")
    dia_str = ', '.join(dia)
    materia_str = ', '.join(materia)