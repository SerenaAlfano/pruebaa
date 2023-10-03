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

