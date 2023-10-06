// script.js

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

    calendarBody.addEventListener("click", (event) => {
        const clickedCell = event.target;

        if (clickedCell.tagName === "TD" && !isNaN(clickedCell.textContent)) {
            const dayNumber = parseInt(clickedCell.textContent, 10);

            const modal = document.getElementById("myModal");
            const closeModal = document.getElementById("modal-close-button");
            const customCloseButton = document.getElementById("custom-close-button");
            const horariosTable = document.getElementById("horarios-table");

            // Hacer una solicitud AJAX para obtener datos de horarios desde el servidor
            fetch('/obtener_horarios_mysql') // Asegúrate de que esta URL coincida con la ruta en tu aplicación Flask
                .then(response => response.json())
                .then(data => {
                    // Llena la tabla de horarios con los datos obtenidos
                    const tablaHTML = data.map(item => `<tr><td>${item.nombre}</td><td>${item.apellido}</td><td>${item.dia}</td><td>${item.horario}</td><td>${item.materia}</td></tr>`).join('');
                    horariosTable.innerHTML = `<tr><th>Nombre</th><th>apellido</th><th>dia</th><th>horario</th><th>materia</th></tr>${tablaHTML}`;
                });

            modal.style.display = "block";

            closeModal.addEventListener("click", () => {
                modal.style.display = "none";
            });

            customCloseButton.addEventListener("click", () => {
                modal.style.display = "none";
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
