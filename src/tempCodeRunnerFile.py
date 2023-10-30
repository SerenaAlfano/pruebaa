    if len(alumno) >= 7:
            materias = "<br/>".join(alumno[6].split(", "))
            dias = "<br/>".join(alumno[4].split(", "))
            data.append([
                Paragraph(alumno[0], styles['Normal']),
                Paragraph(alumno[1], styles['Normal']),
                Paragraph(alumno[2], styles['Normal']),
                Paragraph(alumno[3], styles['Normal']),
                Paragraph(dias, styles['Normal']),
                Paragraph(alumno[5], styles['Normal']),
                Paragraph(materias, styles['Normal'])
            ])
        else:
            # Manejar el caso en el que las tuplas no tienen la cantidad esperada de elementos
            data.append(["", "", "", "", "", "", ""])