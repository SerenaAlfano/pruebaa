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
            const closeModal = document.getElementById("modal-close-button"); // Icono de cierre
            const customCloseButton = document.getElementById("custom-close-button"); // Botón personalizado de cierre

            const modalContent = document.querySelector("#modal-content");
            modalContent.innerHTML = `<p>Detalles para el día ${dayNumber}</p>`;

            modal.style.display = "block";

            // Agregar un evento de clic al icono de cierre para cerrar el modal
            closeModal.addEventListener("click", () => {
                modal.style.display = "none";
            });

            // Agregar un evento de clic al botón personalizado de cierre para cerrar el modal
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
