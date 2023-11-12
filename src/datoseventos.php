<?php 
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header('Content-Type: application/json');

require("conexion.php");

$conexion = regresarConexion();

switch($_GET['accion']) {
    case 'listar':
        $datos = mysqli_query($conexion,"select id,
        titulo as title, 
        descripcion, 
        inicio as start, 
        fin as end,
        colortexto as textColor,
        colorfondo as backgroundColor 
        from eventos");

        $resultado = mysqli_fetch_all ($datos, MYSQLI_ASSOC);
        echo json_encode($resultado);
    
        break;
    
        case 'agregar':
            // Obtener la fecha y hora del nuevo evento
            $inicio = $_POST['inicio'];
            $fin = $_POST['fin'];
        
            // Contar cuántos eventos existen para la misma fecha y hora
            $contarEventos = mysqli_query($conexion, "SELECT COUNT(*) AS cantidad FROM eventos WHERE inicio <= '$inicio' AND fin >= '$fin'");
            $resultadoContador = mysqli_fetch_assoc($contarEventos);
        
            // Verificar si hay menos de 4 eventos para permitir la inserción
            if ($resultadoContador['cantidad'] < 4) {
                $respuesta = mysqli_query($conexion, "INSERT INTO eventos (titulo, descripcion, inicio, fin, colortexto, colorfondo) VALUES 
                ('$_POST[titulo]','$_POST[descripcion]','$inicio','$fin','$_POST[colortexto]','$_POST[colorfondo]')");
                echo json_encode($respuesta);
            } else {
                // Mostrar un mensaje de error
                echo json_encode(array('error' => 'No hay más cupos disponibles para este horario.'));
            }
            break;
        
        
        

        case 'modificar':
            $respuesta = mysqli_query($conexion, "update eventos set titulo = '$_POST[titulo]', 
            descripcion = '$_POST[descripcion]',
            inicio =  '$_POST[inicio]',
            fin = '$_POST[fin]',
            colortexto = '$_POST[colortexto]',
            colorfondo = '$_POST[colorfondo]' 
            where id = '$_POST[id]'");
            echo json_encode($respuesta);
            break;
        

    case 'borrar':
        $respuesta = mysqli_query($conexion,"delete from eventos where id = $_POST[id] ");
        echo json_encode($respuesta); 
        break;
        case 'obtener_alumnos':
            $datos = mysqli_query($conexion, "SELECT id, nombre, apellido FROM alumnos");
            $resultado = mysqli_fetch_all($datos, MYSQLI_ASSOC);
            echo json_encode($resultado);
            break;

}

?>