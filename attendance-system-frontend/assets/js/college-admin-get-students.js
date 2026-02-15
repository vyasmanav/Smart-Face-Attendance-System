const headers = { Authorization: 'Bearer ' + localStorage.getItem("token") }
const table = document.querySelector("#student-table-body")

async function get_students(event) {
    try {
        let students = await axios({
            method: "GET",
            url: "http://localhost:8000/get-students/",
            headers
        })
        console.log(students.data)
        const student_details = students.data
        let i = 1
        for (let student of student_details) {
            console.log(student)
            const html = `
            <tr class="px-10">
            <td data-label="Id">${i}</td>
            <td data-label="Enrollment Number">${student.gr_number || "-"}</td>
            <td data-label="Roll Number">${student.roll_number || "-"}</td>
            <td data-label="Name">${student.user[0].first_name} ${student.user[0].last_name}</td>
            <td data-label="Contect Number">${student.user[0].contact_number}</td>
            <td data-label="Email Id">${student.user[0].email}</td>
            <td data-label="Edit"><a href="college-admin-manage-student-details.html?id=${student.user[0]._id}"><img style="height:20px;width:20px" src="assets/images/pen-to-square-solid.svg"/></a></td>
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
