<?php 
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header('Content-Type: application/json');

require("conexion.php");

$conexion = regresarConexion();

switch($_GET['accion']) {
 //Listar evento
    case 'listar':
        $datos = mysqli_query($conexion, "select id, 
        nombre_alumno as title,
        inicio as start,
        materias, 
        descripcion, 
        colortexto as textColor,
        colorfondo as backgroundColor
        from eventos");

        $resultado = mysqli_fetch_all($datos, MYSQLI_ASSOC);
        echo json_encode($resultado);      
        break;

 //Agregar evento
    case 'agregar':
        
        $nombre_alumno = $_POST['nombre_alumno'];
        $inicio = $_POST['inicio'] . ' ' . $_POST['horario'] . ':00'; 
        // Obtener la lista de materias separadas por comas
        $materias = $_POST['materias'];
        $respuesta = mysqli_query($conexion, "insert into eventos(nombre_alumno,inicio,materias,descripcion,colortexto,colorfondo) values
        ('$nombre_alumno','$inicio','$materias','$_POST[descripcion]',
        '$_POST[colortexto]','$_POST[colorfondo]')");
        echo json_encode($respuesta);    
        break;

// Modificar evento
case 'modificar':
    $inicio = $_POST['inicio'] . ' ' . $_POST['horario'] . ':00'; // Forma la nueva fecha y hora
    $respuesta = mysqli_query($conexion, "UPDATE eventos SET 
        nombre_alumno = '$_POST[nombre_alumno]',
        inicio = '$inicio', // Actualiza el campo 'inicio'
        materias = '$_POST[materias]',

        descripcion = '$_POST[descripcion]',
        colortexto = '$_POST[colortexto]',
        colorfondo = '$_POST[colorfondo]'
        WHERE id = $_POST[id]");
    echo json_encode($respuesta);
    break;

//Borrar evento
    case 'borrar':
        $respuesta = mysqli_query($conexion, "delete from eventos where id = " . $_POST['id']);
        echo json_encode($respuesta);
        break;

        case 'materias':
            $datos = mysqli_query($conexion, "SELECT id, nombre_materia FROM materias");
            $resultado = mysqli_fetch_all($datos, MYSQLI_ASSOC);
            echo json_encode($resultado);
        break;

        case 'alumnos':
    $datos = mysqli_query($conexion, "SELECT nombre, apellido FROM alumnos");
    $resultado = mysqli_fetch_all($datos, MYSQLI_ASSOC);
    echo json_encode($resultado);
    break;

        
}   

?>