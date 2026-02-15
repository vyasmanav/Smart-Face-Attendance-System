
// const Image_upload = document.querySelector("#image_upload");
const submit = document.querySelector(".submit")
const headers = {Authorization:`Bearer ${localStorage.getItem("token")}`}
console.log(headers)

async function Query(event){
    event.preventDefault();
    try {
        payload = { 
            query:query?.value,
        }
        console.log(query,query?.value)
        let Query_info = await axios({
            method:"POST",
            // Name of Student Query
            url:"http://localhost:8000/get-attendance/",
            data:payload,
            headers
        })
        console.log(Query_info)
    } catch (error) {
        console.log(error)
    }
}

submit.addEventListener("click",Query)