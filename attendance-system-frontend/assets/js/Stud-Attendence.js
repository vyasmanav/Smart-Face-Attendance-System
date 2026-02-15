const headers = {Authorization:`Bearer ${localStorage.getItem("token")}`}
const table = document.querySelector(".atte")
console.log(headers)
async function get_attendance_details(event){
	const attendance_details = await axios({
		method:"GET",
		url:`http://localhost:8000/get-attendance`,
		headers
	})
	const data = attendance_details.data
	let id = []
	let subject_names = []
	console.log(data)
	for(const i of data){
		console.log(i)
	const html=`
				<div style="margin-left:50px">
                    <div class="pie animate no-round" style="--p:${i.count};--c:rgb(139, 51, 55);"> 
                        <p>${i.count}<span style=" font-size: 40px;">/80</span></p></div>
                    <p style="margin-left: 40px;">${i._id}</p>
                </div>
	
	`
	table.insertAdjacentHTML("beforeend",html)
	}
}

// get_attendance_details()

window.onload = get_attendance_details