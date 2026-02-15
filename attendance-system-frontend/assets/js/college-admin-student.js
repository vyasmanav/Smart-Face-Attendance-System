const enroll_number = document.querySelector("#enroll_number");
const roll_no = document.querySelector("#roll_no")
const start_year = document.querySelector("#start_year");
const end_year = document.querySelector("#end_year");
const division = document.querySelector("#division")
const update = document.querySelector("#update");
const delete_ = document.querySelector("#delete");
const insert = document.querySelector("#insert");
const studentDropdown = document.querySelector("#student_dropdown");
console.log(studentDropdown,"=========Student Dropdown")
const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
let id = urlParams.get("id")
const headers = {Authorization: "Bearer " + localStorage.getItem("token")}
console.log(id)
const message = document.querySelector(".message")

// Fetch students list and populate dropdown
async function fetchStudents() {
    try {
        const response = await axios({
            method: "GET",
            url: "http://localhost:8000/students/list/",
            headers
        });

        console.log(response,"============response")
        
        // Clear dropdown except the first option
        const firstOption = studentDropdown.options[0];
        studentDropdown.innerHTML = '';
        studentDropdown.appendChild(firstOption);
        
        // Populate dropdown with students
        if (response.data && Array.isArray(response.data.students)) {
            response.data.students.forEach(student => {
                const option = document.createElement('option');
                option.value = student._id;
                option.textContent = `${student.first_name} ${student.last_name}`;
                studentDropdown.appendChild(option);
            });
        }
    } catch (error) {
        console.error("Error fetching students:", error);
        const html = `<div class="alert alert-danger" role="alert">
        Failed to load students list. Please try again.
        </div>`;
        message.innerHTML = html;
    }
}

// Load students when page loads
document.addEventListener('DOMContentLoaded', fetchStudents);

// Update form fields when a student is selected
studentDropdown.addEventListener('change', function() {
    const selectedStudentId = this.value;
    if (selectedStudentId) {
        // You can optionally load additional student details here if needed
        console.log("Selected student ID:", selectedStudentId);
        id = selectedStudentId;
    }
});

async function Insert_student(event) {
    event.preventDefault();
    try {
        const selectedStudentId = studentDropdown.value;
        if (!selectedStudentId) {
            alert("Please select a student from the dropdown");
            return;
        }
        
        payload = {
            student_id: selectedStudentId,  
            division_id: division.value,
            gr_number: enroll_number.value,
            roll_number: roll_no.value,
            admission_date: start_year.value,
            admission_valid_date: end_year.value,
        }
        console.log(payload)
        for (const data in payload) {
            if (payload[data] === ""){
                error_message = "Invalid Data"
                alert("Please make sure that any of that field is not empty")
                return
            }
        }
        console.log(payload)
        let Insert_info = await axios({
            method: "POST",
            // Name of Insert Student
            url: `http://localhost:8000/manage-student/${id}/`,
            data: payload,
            headers
        })
        console.log(Insert_info)
        const html = `<div class="alert alert-success" role="alert">
        ${Insert_info.data.message}
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        console.log(Insert_info)
    } catch (error) {
        console.log(error)
        const html = `<div class="alert alert-primary" role="alert">
        <span id = "message" style="color:red">${error.response.data.message}</span>
        </div>`
        console.log(error)
        console.log(html)
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
    }
}

insert.addEventListener("click", Insert_student)


async function Update_student(event) {
    event.preventDefault();
    try {
        const selectedStudentId = studentDropdown.value;
        if (!selectedStudentId) {
            alert("Please select a student from the dropdown");
            return;
        }
        
        payload = {
            student_id: selectedStudentId,  
            division_id: division.value,
            gr_number: enroll_number.value,
            roll_number: roll_no.value,
            admission_date:start_year.value,
            admission_valid_date:end_year.value
        }
        // console.log(data)
        for(const data in payload){
            if(payload[data] === "")
                delete payload[data]
        }
        console.log(payload)
        let Update_info = await axios({
            method: "PATCH",
            // Name of Manage timetable
            url: `http://localhost:8000/manage-student/${id}/`,
            data: payload,
            headers
        })
        const html = `<div class="alert alert-success" role="alert">
        ${Update_info.data.message}
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        console.log(Update_info)
    } catch (error) {
        console.log(error)
        const html = `<div class="alert alert-primary" role="alert">
        <span id = "message" style="color:red">${error.response.data.message}</span>
        </div>`
        console.log(html)
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
    }
}

update.addEventListener("click", Update_student)



async function Delete_student(event) {
    event.preventDefault();
    try {
        let Delete_info = await axios({
            method: "DELETE",
            // Name of Manage timetable
            url: `http://localhost:8000/manage-student/${id}/`,
            headers
        })
        const html = `<div class="alert alert-success" role="alert">
        ${Delete_info.data.message}
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        console.log(Delete_info)
    } catch (error) {
        console.log(error)
        const html = `<div class="alert alert-primary" role="alert">
        <span id = "message" style="color:red">${error.response.data.message}</span>
        </div>`
        console.log(html)
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
    }
}

delete_.addEventListener("click", Delete_student)