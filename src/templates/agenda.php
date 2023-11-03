<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agenda</title>

<!-- Scripts CSS -->
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="/static/css/bootstrap.min.css">
<link rel="stylesheet" href="/static/css/datatables.min.css">
<link rel="stylesheet" href="/static/css/bootstrap-clockpicker.css">


<!-- Scripts JS -->
<script src="/static/js/jquery-3.7.1.min.js"></script>
<script src="/static/js/popper.min.js"></script>
<script src="/static/js/bootstrap.min.js"></script>
<script src="/static/js/datatables.min.js"></script>
<script src="/static/js/bootstrap-clockpicker.js"></script>
<script src="/static/js/moment-with-locales.js"></script>
<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>

</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light " style="background-color: #7ea56a;">
        <div class="container-fluid ">
            <a href="{{ url_for('inicio') }}">
                <img src="/static/img/logo.png" alt="Logo" >
            </a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
            <ul class="navbar-nav mx-auto text-center ">
              <li class="nav-item">
                <a class="nav-link " href="{{url_for('alta')}}">
                    Alumnos
                </a> 
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{{url_for('listado')}}">
                    Mis alumnos
                </a> 
              </li>
              <li class="nav-item">
                <a class="nav-link " href="{{url_for('ingresos')}}">
                    Ingresos
                </a> 
              </li>
              <li class="nav-item">
                <a class="nav-link " href="{{url_for('egresos')}}">
                    Egresos
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{{url_for('caja')}}">
                    Caja
                </a> 
              </li>
              <li class="nav-item">
                <a class="nav-link" href="{{url_for('agenda')}}">
                    Agenda
                </a> 
              </li>
              
            </ul>
           
            <div class="text-center ">
                <a class="nav-link" href="{{ url_for('logout') }}">Cerrar Sesión</a>  
              </div>
          </div>
        </div>
      </nav>
  <div class="container-fluid">
    <section class="content-header p-2">
      <h3 class="text-left subtitulo ">Calendario de clases</h3>
    </section>
    <div class="row">
      <div class="col-12">
        <div id="Calendario1" style="border:1px solid #E2E2E2; padding: 2px;"  class="p-2"> </div>
      </div>
      

    </div>
  </div>
  |
    <!-- Formulario de eventos -->
    <div class="modal fade" id="FormularioEventos" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-md" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close " style=" color: #7ea56a: background-color:#fffff; border:none; font-size: 1.5em" data-bs-dismiss="modal" aria-label = "close"> 
              <span aria-hidden="true">x</span>
            </button>
          </div>
          <div class="modal-body ">
            <input type="hidden" id="Id">
            <div class="row">    
              <div class="col-md-4">       
                <label for="">Alumno:</label>
                  <select id="NombreAlumno"  name="nombre_alumno" class="form-modal-calendario">
                      <!-- Opciones para seleccionar al alumno -->                    
                  </select>  
              </div>            
              <div class="col-md-4">  
                <label for="">Fecha:</label>
                <div class="input-group" data-autoclose="true">
                  <input type="date" id="FechaInicio"  value=""  class="form-modal-calendario">
                </div>         
              </div>
              <div class="col-md-4" id="TituloHoraInicio">
                <label for="">Horario:</label>
                <div class="input-group clockpicker" data-autoclose="true">
                    <input type="time" id="Horario" value=""  autocomplete="off"  class="form-modal-calendario">
                </div>
              </div>
            </div>          
            <div class="row mt-2">             
              <label for="">Materias</label>
                <div id="materias-checkbox">
                    <!-- Las materias se generarán aquí dinámicamente -->
                </div>
            </div>
            <div class="row mt-2">   
              <label for="">Descripción</label>
              <textarea id="Descripcion"  rows="3"  class="form-modal-calendario"></textarea>           
            </div>                        
            <div class="row mt-2">  
              <div class="col-6">
              <label for="">Color de fondo:</label>
              <input type="color"  id="ColorFondo"  class="form-modal-calendario" style="height: 15px;"></input>
              </div>
              <div class="col-6">
              <label for="">Color de texto:</label>
              <input type="color"  id="ColorTexto"  class="form-modal-calendario" style="height: 15px;"></input>
            </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" id="BotonAgregar" class="btn-guardar">Agregar</button>
            <button type="button" id="BotonModificar" class="btn btn-success">Modificar</button>
            <button type="button" id="BotonBorrar" class="btn-guardar" style="background:#7ea56a;">Borrar</button>
            <button type="button" class="btn btn-success" data-bs-dismiss="modal">Cancelar</button>
          </div>
        </div>

      </div>
    </div>
  
  <script>
    document.addEventListener("DOMContentLoaded", function(){
     
    let calendario1 = new FullCalendar.Calendar(document.getElementById('Calendario1'),{
      height: 500,
      headerToolbar:{
        left: 'prev,next today',
        center: 'title',
        right:'dayGridMonth,timeGridWeek,timeGridDay',
      },
      editable: true,
      events: 'http://localhost/prueba/pruebaa/src/datoseventos.php?accion=listar',
      dateClick: function(info){
        limpiarFormulario();
        $('#BotonAgregar').show();
        $('#BotonModificar').hide();
        $('#BotonBorrar').hide();

        if (info.allDay){
          $('#FechaInicio').val(info.dateStr)
        }else{
          let fechaHora = info.dateStr.split("T");
          $('#FechaInicio').val(fechaHora[0]);
          $('#HoraInicio').val(fechaHora[1].substring(0,5));
        }

        $("#FormularioEventos").modal('show'); 
      },
      eventClick: function(info){
        $('#BotonAgregar').hide();  
        $('#BotonModificar').show();
        $('#FormularioBorrar').show();

        $('#Id').val(info.event.id);
        $('#nombre_alumno').val(info.event.title);
        $('#FechaInicio').val(moment(info.event.start).format("YYYY-MM-DD"));
        $('#Horario').val(moment(info.event.start).format("HH:mm"));
        $('#Materias').val(info.event.extendedProps.materias);
        $('#Descripcion').val(info.event.extendedProps.descripcion);
        $('#ColorFondo').val(info.event.backgroundColor);
        $('#ColorTexto').val(info.event.textColor);
       $("#FormularioEventos").modal('show')  
      },
      
      eventDrop: function(info){
        $('#Id').val(info.event.id);
        $('#nombre_alumno').val(info.event.title);
        $('#FechaInicio').val(moment(info.event.start).format("YYYY-MM-DD"));
        $('#Horario').val(moment(info.event.start).format("HH:mm"));
        $('#Materias').val(info.event.extendedProps.materias);
        $('#Descripcion').val(info.event.extendedProps.descripcion);
        $('#ColorFondo').val(info.event.backgroundColor);
        $('#ColorTexto').val(info.event.textColor);  
        let registro = recuperarDatosFormulario();
        modificarRegistro(registro);
      }     
      }
    );
    
    calendario1.render();


    //Eventos de botones 
    // Boton Agregar
    $('#BotonAgregar').click(function () {
            let registro = recuperarDatosFormulario();
            agregarRegistro(registro);
            $('#FormularioEventos').modal('hide');
        });

        // Boton Modificar
        $('#BotonModificar').click(function () {
            let registro = recuperarDatosFormulario();
            modificarRegistro(registro);
            $('#FormularioEventos').modal('hide');
        });

        // Boton Borrar
        $('#BotonBorrar').click(function () {
            let registro = recuperarDatosFormulario();
            borrarRegistro(registro);
            $('#FormularioEventos').modal('hide');
        });



   // Funciones para comunicarse con el servidor AJAX!
   function agregarRegistro(registro) {
            $.ajax({
                type: 'POST',
                url: 'http://localhost/prueba/pruebaa/src/datoseventos.php?accion=agregar',
                data: registro,
                success: function (msg) {
                    calendario1.refetchEvents();
                },
                error: function (error) {
                    alert("Hubo un error al agregar el alumno:" + error);
                }
            });
        }

        function modificarRegistro(registro) {
            $.ajax({
                type: 'POST',
                url: 'http://localhost/prueba/pruebaa/src/datoseventos.php?accion=modificar',
                data: registro,
                success: function (msg) {
                    calendario1.refetchEvents();
                },
                error: function (error) {
                    alert("Hubo un error al modificar el alumno:" + error);
                }
            });
        }

        function borrarRegistro(registro) {
            $.ajax({
                type: 'POST',
                url: 'http://localhost/prueba/pruebaa/src/datoseventos.php?accion=borrar',
                data: registro,
                success: function (msg) {
                    calendario1.refetchEvents();
                },
                error: function (error) {
                    alert("Hubo un error al borrar el alumno: " + JSON.stringify(error));
                }
            });
        }

        // Funciones que interactúan con el formulario eventos
        function limpiarFormulario() {
            $('#Id').val('');
            var nombreAlumno = $('#NombreAlumno').val();
            $('#FechaInicio').val('');
            $('#Horario').val('');
            $('#Materias').val('');
            $('#Descripcion').val('');
            $('#ColorFondo').val('#FBD374');
            $('#ColorTexto').val('#ffffff');
        }

        function recuperarDatosFormulario() {
            let registro = {
                id: $('#Id').val(),
                nombre_alumno: $('#NombreAlumno').val(),
                inicio: $('#FechaInicio').val(),
                horario: $('#Horario').val(),
                materias: $('#Materias').val(),
                descripcion: $('#Descripcion').val(),
                colorfondo: $('#ColorFondo').val(),
                colortexto: $('#ColorTexto').val()
            };
            return registro;
        }

        // Antes de mostrar el modal, obtén las materias de la base de datos
        $("#FormularioEventos").on('show.bs.modal', function () {
    $.ajax({
        url: 'http://localhost/prueba/pruebaa/src/datoseventos.php?accion=materias',
        method: 'GET',
        success: function (data) {
            var materiasCheckbox = $('#materias-checkbox');
            materiasCheckbox.empty();

            for (var i = 0; i < data.length; i += 2) {
                var checkboxRow = '<div class="row">';

                // Checkbox 1
                if (data[i]) {
                    checkboxRow += `
                        <div class="form-check col-6">
                            <input class="form-check-input" type="checkbox" name="materias[]" value="${data[i].id}" id="materia${data[i].id}">
                            <label class="form-check-label" for="materia${data[i].id}">
                                ${data[i].nombre_materia}
                            </label>
                        </div>`;
                }

                // Checkbox 2
                if (data[i + 1]) {
                    checkboxRow += `
                        <div class="form-check col-6">
                            <input class="form-check-input" type="checkbox" name="materias[]" value="${data[i + 1].id}" id="materia${data[i + 1].id}">
                            <label class="form-check-label" for="materia${data[i + 1].id}">
                                ${data[i + 1].nombre_materia}
                            </label>
                        </div>`;
                }

                checkboxRow += '</div>';
                materiasCheckbox.append(checkboxRow);
            }
        },
        error: function (error) {
            console.error('Error al obtener las materias: ' + JSON.stringify(error));
        }
    });
});


        // Antes de mostrar el modal, obtén la lista de alumnos de tu tabla "alumnos"
        $("#FormularioEventos").on('show.bs.modal', function () {
            $.ajax({
                url: 'http://localhost/prueba/pruebaa/src/datoseventos.php?accion=alumnos',
                method: 'GET',
                success: function (data) {
                    var nombreAlumnoSelect = $('#NombreAlumno');
                    nombreAlumnoSelect.empty();

                    data.forEach(function (alumno) {
                        var option = `<option value="${alumno.nombre} ${alumno.apellido}">${alumno.nombre} ${alumno.apellido}</option>`;
                        nombreAlumnoSelect.append(option);
                    });
                },
                error: function (error) {
                    console.error('Error al obtener la lista de alumnos: ' + JSON.stringify(error));
                }
            });
});
});



  </script>
  
</body>
</html>