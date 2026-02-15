const semester_details = document.querySelector("#semester");
const subject_details = document.querySelector("#subject");
const faculty_details = document.querySelector("#faculty")
const division_details = document.querySelector("#division");
const room_number = document.querySelector("#room_number");
const start_time = document.querySelector("#appt1")
const end_time = document.querySelector("#appt");
const remark = document.querySelector("#remark");
const update = document.querySelector("#update");
const delete_ = document.querySelector("#delete");
const headers = { Authorization: 'Bearer ' + localStorage.getItem("token") };
const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const id = urlParams.get("id")
const message = document.querySelector(".message")

async function get_required_details(event){
    try {
        const details = await axios({
            method:"GET",
            url:"http://localhost:8000/get-required-timetable-details/",
            headers
        })
        const data = details.data
        // semester_details.innerHTML = `<option value="">Select Semester</option>`

        for(semester of data.semester_details){
            let option = document.createElement("option")
            option.value = semester._id
            option.innerText = semester.semester_name
            semester_details.insertAdjacentElement("beforeend",option)
        }

        for(subject of data.subject_details){
            let option = document.createElement("option")
            option.value = subject._id
            option.innerText = subject.subject_name
            subject_details.insertAdjacentElement("beforeend",option)
        }

        for(faculty of data.faculty_details){
            let option = document.createElement("option")
            option.value = faculty._id
            option.innerText = `${faculty.first_name} ${faculty.last_name}`
            faculty_details.insertAdjacentElement("beforeend",option)
        }

        for(division of data.division_details){
            let option = document.createElement("option")
            option.value = division._id
            option.innerText = division.division_name
            division_details.insertAdjacentElement("beforeend",option)
        }

    } catch (error) {
        console.log(error)
    }
}

window.onload = get_required_details

async function Upadte_timetable(event) {
    event.preventDefault();
    try {
        payload = {
            subject_id: subject_details.value,
            faculty_id: faculty_details.value,
            division: division_details.value,
            room_number: room_number.value,
            start_time: start_time.value,
            end_time: end_time.value,
            remarks: remark.value,
            semester_id:semester_details.value
        }
        for (const data in payload) {
            if (payload[data] === "")
                delete payload[data]
        }
        let Update_info = await axios({
            method: "PATCH",
            // Name of Manage timetable
            url: `http://localhost:8000/manage-timetable/${id}/`,
            data: payload,
            headers
        })
        console.log(Update_info)
        const html = `<div class="alert alert-success" role="alert">
        ${Update_info.data.message}
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
    } catch (error) {
        const html = `<div class="alert alert-primary" role="alert">
        <span id = "message" style="color:red">${error.response.data.message}</span>
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        console.log(error)
    }
}

update.addEventListener("click", Upadte_timetable)



async function Delete_timetable(event) {
    event.preventDefault();
    try {
        let Update_info = await axios({
            method: "DELETE",
            // Name of Manage timetable
            url: `  http://localhost:8000/manage-timetable/${id}/`,
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
    }
}

delete_.addEventListener("click", Delete_timetable)