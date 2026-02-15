const query = document.querySelector(".query");
// const Image_upload = document.querySelector("#image_upload");
const submit = document.querySelector("#submit")
const headers = {Authorization:`Bearer ${localStorage.getItem("token")}`}
console.log(headers)
const message = document.querySelector(".message")

async function Query(event){
    event.preventDefault();
    try {
        payload = {
            query:query?.value,
        }
        for (const data in payload) {
            if (payload[data] === ""){
                error_message = "Invalid Data"
                alert("Please make sure that any of that field is not empty")
                return
            }
        }
        console.log(query,query?.value)
        let Query_info = await axios({
            method:"POST",
            // Name of Student Query
            url:"http://localhost:8000/query/",
            data:payload,
            headers
        })

        const html = `<div class="alert alert-success" role="alert">
        Success Uploaded
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        console.log(data)
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