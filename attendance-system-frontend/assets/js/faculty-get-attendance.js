const headers = { Authorization: 'Bearer ' + localStorage.getItem("token") }
const table = document.querySelector("#attendance-table-body")


async function get_students(event) {
    try {
        let attendance_details = await axios({
            method: "GET",
            url: "http://localhost:8000/get-attendance/",
            headers
        })
        let i = 1
        console.log(attendance_details.data)
        attendance_details = attendance_details.data

        

        for (let attendance of attendance_details) {
            console.log(attendance)
            const html = `
            <tr class="px-10">
            <input type="hidden" value="${attendance._id}" class="attendance-id">
            <td data-label="Id">${i}</td>
            <td data-label="Enrollment Number">${attendance.student_details.gr_number || "-"}</td>
            <td data-label="Roll Number">${attendance.student_details.roll_number || "-"}</td>
            <td data-label="Roll Number">${attendance.user.first_name || "-"} ${attendance.user.last_name || ""}</td>
            <td data-label="Submit"><button class="template-btn present-attendance">Present</button></td>
            </tr>
            `
            table.insertAdjacentHTML("beforeend",html)
            i++
        }
    } catch (error) {
        console.log(error)
    }
}

window.onload = get_students

const correct_attendance_handler = async (event)=>{
    if(event.target.classList.contains("present-attendance")){
        const attendanceID = event.target.closest("tr").querySelector(".attendance-id").value
        console.log('Attendance ID:', attendanceID);
        console.log(event.target.closest("tr"))
        try {
            let attendance_change_details = await axios({
                method:"GET",
                url:`http://localhost:8000/correct-attendance/${attendanceID}/`,
                headers
            })
            event.target.closest("tr").remove()
            console.log(attendance_change_details)
        } catch (error) {
            console.log(error)
        }
    }
}

table.addEventListener("click",correct_attendance_handler)