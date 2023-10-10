@app.route('/descargar_lista_alumnos_pdf')
def descargar_lista_alumnos_pdf():
    # Obtén los datos de todos los alumnos en tu base de datos
    cursor = db_connection.cursor()
    cursor.execute("SELECT nombre, apellido, curso, nivel_educativo, dia, horario, materia FROM alumnos")
    alumnos = cursor.fetchall()
    cursor.close()

    # Configura el búfer de bytes para el PDF
    pdf_buffer = BytesIO()

    # Crea un objeto SimpleDocTemplate para el PDF
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Crea una lista para almacenar los elementos del PDF
    elements = []

    # Agrega un título centrado al PDF
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title = Paragraph('<center><b>Listado de Alumnos</b></center>', title_style)
    elements.append(title)

    # Agrega un espacio en blanco como separación entre el título y la tabla
    elements.append(Spacer(1, 20))

    # Crea una lista para almacenar los datos de los alumnos
    data = [['Nombre', 'Apellido', 'Curso', 'Nivel Educativo', 'Día', 'Horario', 'Materia']]

    for alumno in alumnos:
        data.append([
            alumno[0],  # Nombre
            alumno[1],  # Apellido
            alumno[2],  # Curso
            alumno[3],  # Nivel Educativo
            alumno[4],  # Día
            alumno[5],  # Horario
            alumno[6]   # Materia
        ])

    # Crea una tabla para mostrar los datos de los alumnos
    table = Table(data)

    # Establece el estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
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