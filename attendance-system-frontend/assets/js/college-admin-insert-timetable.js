const semester_details = document.querySelector("#semester")
const division_details = document.querySelector("#division")
const faculty_details = document.querySelector("#faculty")
const subject_details = document.querySelector("#subject")
const room_number = document.querySelector("#room_number")
const start_time = document.querySelector("#start_time")
const end_time = document.querySelector("#end_time")
const remarks = document.querySelector("#remark")
const date = document.querySelector("#date")
const form_submit_button = document.querySelector(".insert_timetable")
const message = document.querySelector(".message")
const headers = {"Authorization":`Bearer ${localStorage.getItem("token")}`}

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

async function form_submit_handler(event){
    event.preventDefault()
    
    // all_fields = ("subject_id", "faculty_id", "division",
    //               "semester_id", "remarks", "room_number", "start_time", "end_time")
    const payload = {
        subject_id:subject_details.value,
        faculty_id:faculty_details.value,
        division:division_details.value,
        semester_id:semester_details.value,
        remarks:remarks.value,
        room_number:room_number.value,
        start_time:start_time.value,
        end_time:end_time.value,
        date:new Date(date.value)
    }

    for (const data in payload) {
        if (payload[data] === ""){
            error_message = "Invalid Data"
            alert("Please make sure that any of that field is not empty")
            return
        }
    }

    try {
        const insert_timetable = await axios({
            method:"POST",
            url:"http://localhost:8000/manage-timetable/",
            data:payload,
            headers
        })
        const html = `<div class="alert alert-success" role="alert">
        ${insert_timetable.data.message}
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        console.log(insert_timetable.data.message)
    } catch (error) {
        const html = `<div class="alert alert-primary" role="alert">
        <span id = "message" style="color:red">${error.response.data.message}</span>
        </div>`
        console.log(html)
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        console.log(error.message)
    }


    console.log(payload)
}

form_submit_button.addEventListener("click",form_submit_handler)
window.onload = get_required_details