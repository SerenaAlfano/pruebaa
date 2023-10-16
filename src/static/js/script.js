document.addEventListener('DOMContentLoaded', function () {
    const calendarBody = document.getElementById("calendar-body");
    const monthYear = document.getElementById("month-year");
    const prevMonth = document.getElementById("prev-month");
    const nextMonth = document.getElementById("next-month");

    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    function updateCalendar() {
        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
        const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

        calendarBody.innerHTML = "";
        monthYear.textContent = new Date(currentYear, currentMonth).toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });

        let day = 1;
        for (let i = 0; i < 6; i++) {
            const row = document.createElement("tr");
            for (let j = 0; j < 7; j++) {
                if ((i === 0 && j < firstDayOfMonth) || day > daysInMonth) {
                    const cell = document.createElement("td");
                    row.appendChild(cell);
                } else {
                    const cell = document.createElement("td");
                    cell.textContent = day;
                    row.appendChild(cell);
                    day++;
                }
            }
            calendarBody.appendChild(row);
        }
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
            const formattedDate = selectedDate.toISOString().split("T")[0];

            const modal = document.getElementById("myModal");
            const horariosTable = document.getElementById("horarios-table");

            // Realiza una solicitud AJAX para obtener los datos del alumno desde el servidor
            fetch(`/obtener_horarios?fecha=${formattedDate}`) // Ajusta la ruta según tu configuración
                .then(response => response.json())
                .then(data => {
                    // Llena la tabla de horarios con los datos obtenidos
                    horariosTable.innerHTML = `<tr><th>Nombre</th><th>Apellido</th><th>Día</th><th>Horario</th><th>Materia</th></tr>
                        <tr><td>${data.nombre}</td><td>${data.apellido}</td><td>${data.dia}</td><td>${data.horario}</td><td>${data.materia}</td></tr>`;
                });

            modal.style.display = "block";
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

