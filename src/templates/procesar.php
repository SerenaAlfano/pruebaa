<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Recibir datos del formulario
    $nombre = $_POST['nombre_alumno'];
    $dni = $_POST['dni'];
    $fecha = $_POST['fecha'];
    $total = $_POST['total'];
    $mediodepago = $_POST['mediosdepago'];
    $descripcion = $_POST['descripcion'];

    $recibo = "
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <title>Recibo de Pago</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                padding: 20px;
            }
            .receipt {
                max-width: 600px;
                margin: 0 auto;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                padding: 20px;
            }
            h2 {
                background-color: #333;
                color: #fff;
                padding: 10px;
                text-align: center;
            }
            .details {
                margin-top: 20px;
                padding: 10px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
            }
            .details p {
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class='receipt'>
            <h2>Recibo de Pago</h2>
            <div class='details'>
                <p><strong>Nombre:</strong> $nombre</p>
                <p><strong>DNI:</strong> $dni</p>
                <p><strong>Fecha:</strong> $fecha</p>
                <p><strong>Descripción:</strong> $descripcion</p>
                <p><strong>Total:</strong> $$total</p>
                <p><strong>Medio de Pago:</strong> $mediodepago</p>
            </div>
        </div>
    </body>
    </html>
    ";

    // Set the content type to HTML
    header('Content-Type: text/html');

    // Imprimir el recibo
    echo $recibo;
}
?>

