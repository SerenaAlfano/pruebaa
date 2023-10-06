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
// Agregar un evento de clic a los números del calendario
calendarBody.addEventListener("click", (event) => {
    const clickedCell = event.target;
    
    // Verificar si se hizo clic en un número (td con contenido numérico)
    if (clickedCell.tagName === "TD" && !isNaN(clickedCell.textContent)) {
        const dayNumber = parseInt(clickedCell.textContent, 10);
        
        // Obtener el modal y el botón de cierre
        const modal = document.getElementById("myModalagenda");
        const closeModal = document.getElementsByClassName("close")[0];
        
        // Establecer el contenido del modal (personalízalo según tus necesidades)
        const modalContent = document.querySelector(".modal-content");
        modalContent.innerHTML = `<p>Detalles para el día ${dayNumber}</p>`;
        
        // Mostrar el modal
        modal.style.display = "block";
        
        // Agregar un evento de clic al botón de cierre para cerrar el modal
        closeModal.addEventListener("click", () => {
            modal.style.display = "none";
        });
    }
});