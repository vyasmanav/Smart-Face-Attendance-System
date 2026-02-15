const query_el = document.querySelector("#query");
const answer = document.querySelector("#Answer");
const submit = document.querySelector("#submit")
const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const id = urlParams.get("id")
const message = document.querySelector(".message")

const headers = { Authorization: `Bearer ${localStorage.getItem("token")}` };

async function load_query(){
    try {
        const query = await axios({
            method:"GET",
            url:`http://localhost:8000/get-queries/${id}/`,
            headers
        })
        query_el.value = query.data.query
        console.log(query)
    } catch (error) {
        console.log(error.message)
    }
}

window.onload = load_query

async function Query(event){
    event.preventDefault();
    try {
        payload = {
            answer:answer.value,
        }
        for (const data in payload) {
            if (payload[data] === ""){
                error_message = "Invalid Data"
                alert("Please make sure that any of that field is not empty")
                return
            }
        }
        let Query_info = await axios({
            method:"POST",
            // Name of Faculty Query
            url:`http://localhost:8000/answer-query/${id}/`,
            data:payload,
            headers
        })
        const html = `<div class="alert alert-success" role="alert">
        Answer Uploaded
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        console.log(data)
        console.log(Query_info)
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

submit.addEventListener("click",Query)