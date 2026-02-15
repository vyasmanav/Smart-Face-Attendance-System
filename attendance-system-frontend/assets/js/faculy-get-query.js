const headers = { Authorization: 'Bearer ' + localStorage.getItem("token") }
const table = document.querySelector("#student-table-body")

async function get_query(event) {
    try {
        let students = await axios({
            method: "GET",
            url: "http://localhost:8000/get-queries/",
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
            <td data-label="Enrollment Number">${student.student.gr_number || "-"}</td>
            <td data-label="Roll Number">${student.student.roll_number || "-"}</td>
            <td data-label="Name"><a href="faculty-query.html?id=${student._id}">${student.user.first_name} ${student.user.last_name}</a></td>
            <td data-label="Contect Number">${student.user.email}</td>
            <td data-label="query">${student.query}</td>
            <td data-label="date">${student.query_raised_date}</td>
            </tr>
            `
            table.insertAdjacentHTML("beforeend",html)
            i++
        }
    } catch (error) {
        console.log(error)
    }
}


// change
window.onload = get_query 
