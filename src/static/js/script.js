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

            // Llena la tabla de horarios con contenido dinámico (en este ejemplo, horarios ficticios)
            horariosTable.innerHTML = `
                <tr>
                    <th>nombre</th>
                    <th>apellido</th>
                    <th>dia</th>
                    <th>horario</th>
                    <th>materia</th>
                </tr>
            `;

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
