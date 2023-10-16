document.addEventListener('DOMContentLoaded', function () {
    const calendarBody = document.getElementById("calendar-body");
    const monthYear = document.getElementById("month-year");
    const prevMonth = document.getElementById("prev-month");
    const nextMonth = document.getElementById("next-month");

    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    // Función para obtener la disponibilidad desde la base de datos
    function obtenerDisponibilidad() {
        return fetch(`/obtener_disponibilidad`) // Ajusta la ruta según tu configuración
            .then(response => response.json());
    }

    function updateCalendar() {
        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
        const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

        calendarBody.innerHTML = "";
        monthYear.textContent = new Date(currentYear, currentMonth).toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });

        obtenerDisponibilidad().then(disponibilidad => {
            let day = 1;
            for (let i = 0; i < 6; i++) {
                const row = document.createElement("tr");
                for (let j = 0; j < 7; j++) {
                    const cell = document.createElement("td");
                    if (day <= daysInMonth) {
                        cell.textContent = day;
                        const date = new Date(currentYear, currentMonth, day);
                        const formattedDate = date.toISOString().split('T')[0]; // Formato ISO 8601
                        if (disponibilidad.includes(formattedDate)) {
                            // Aplica un estilo especial a los días disponibles
                            cell.classList.add('dia-disponible');
                        }
                        day++;
                    }
                    row.appendChild(cell);
                }
                calendarBody.appendChild(row);
            }
        });
    }

    updateCalendar();

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            const modal = document.getElementById("myModal");
            modal.style.display = "none";
        }
    });

    calendarBody.addEventListener("click", (event) => {
        const clickedCell = event.target;

        if (clickedCell.tagName === "TD" && !isNaN(clickedCell.textContent)) {
            const dayNumber = parseInt(clickedCell.textContent, 10);
            const selectedDate = new Date(currentYear, currentMonth, dayNumber);

            // Formatea la fecha seleccionada en el formato deseado (por ejemplo, ISO 8601)
            const formattedDate = selectedDate.toISOString();

            const modal = document.getElementById("myModal");
            const horariosTable = document.getElementById("horarios-table");

            // Realiza una solicitud AJAX para obtener los datos del alumno desde el servidor
            fetch(`/obtener_alumno?fecha=${formattedDate}`) // Ajusta la ruta según tu configuración
                .then(response => response.json())
                .then(data => {
                    // Llena la tabla de horarios con los datos obtenidos
                    horariosTable.innerHTML = `<tr><th>Nombre</th><th>Apellido</th><th>Día</th><th>Horario</th><th>Materia</th></tr>
                        <tr><td>${data.nombre}</td><td>${data.apellido}</td><td>${data.dia}</td><td>${data.horario}</td><td>${data.materia}</td></tr>`;
                    
                    // Abre el modal
                    modal.style.display = "block";
                });
        }
    });

    prevMonth.addEventListener("click", () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentYear--;
            currentMonth = 11;
        }
        updateCalendar();
    });

    nextMonth.addEventListener("click", () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentYear++;
            currentMonth = 0;
        }
        updateCalendar();
    });
});

