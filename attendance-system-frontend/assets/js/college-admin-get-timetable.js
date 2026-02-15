const headers = { Authorization: 'Bearer ' + localStorage.getItem("token") }
const table = document.querySelector("#time-table-body")

async function get_students(event) {
    try {
        let lectures = await axios({
            method: "GET",
            url: "http://localhost:8000/get-timetable/",
            headers
        })
        console.log(lectures.data)
        lectures = lectures.data
        let i = 1
        for (let lecture of lectures) {
            console.log(lecture)
            let date = new Date(lecture.date)
            const html = `
            <tr class="px-10">
            <td data-label="Id">${i}</td>
            <td data-label="Start Time">${lecture.start_time || "-"}</td>
            <td data-label="End Time">${lecture.end_time || "-"}</td>
            <td data-label="Roll Number">${date.getDate() || "-"}-${date.getMonth()}-${date.getFullYear()}</td>
            <td data-label="Room number">${lecture.room_number || "-"}</td>
            <td data-label="Lecture">${lecture.subject.subject_name || "-"}</td>
            <td data-label="Faculty">${lecture.faculty.first_name || "-"} ${lecture.faculty.last_name}</td>
            <td data-label="Division">${lecture.division.division_name || "-"}</td>
            <td data-label="Semester">${lecture.semester.semester_name || "-"}</td>
            <td data-label="Remark">${lecture.remarks || "-"}</td>
            <td data-label="Edit"><a href="/college-admin-manage-timetable.html?id=${lecture._id}"><img style="height:20px;width:20px" src="assets/images/pen-to-square-solid.svg"/></a></td>

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
