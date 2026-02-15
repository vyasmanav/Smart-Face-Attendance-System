const timetableDropdown = document.querySelector("#timetable_dropdown");
const imageInput = document.querySelector("#imageInput");
const form = document.querySelector("#uploadForm");
const message = document.querySelector(".message");
const headers = {Authorization: "Bearer " + localStorage.getItem("token")};

// Fetch timetables and populate dropdown
async function fetchTimetables() {
    try {
        const response = await axios({
            method: "GET",
            url: "http://localhost:8000/list-timetables/",
            headers
        });

        // Clear dropdown except the first option
        const firstOption = timetableDropdown.options[0];
        timetableDropdown.innerHTML = '';
        timetableDropdown.appendChild(firstOption);

        // Populate dropdown with timetables
        if (response.data && Array.isArray(response.data.timetables)) {
            response.data.timetables.forEach(timetable => {
                const option = document.createElement('option');
                option.value = timetable._id;
                option.textContent = `${timetable.subject_details.subject_name} - ${new Date(timetable.date).toLocaleDateString()} - ${timetable.start_time} to ${timetable.end_time}`;
                timetableDropdown.appendChild(option);
            });
        }
    } catch (error) {
        console.error("Error fetching timetables:", error);
        const html = `<div class="alert alert-danger" role="alert">
        Failed to load timetables. Please try again.
        </div>`;
        message.innerHTML = html;
    }
}

// Load timetables when page loads
document.addEventListener('DOMContentLoaded', fetchTimetables);

// Handle form submission
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    try {
        const selectedTimetableId = timetableDropdown.value;
        const file = imageInput.files[0];

        if (!selectedTimetableId) {
            alert("Please select a lecture from the dropdown");
            return;
        }

        if (!file) {
            alert("Please select an image file");
            return;
        }

        // Create FormData
        const formData = new FormData();
        formData.append('timetable_id', selectedTimetableId);
        formData.append('class-frames', file);

        // Send request
        const response = await axios({
            method: "POST",
            url: `http://localhost:8000/attendance/${selectedTimetableId}/`,
            data: formData,
            headers: {
                ...headers,
                'Content-Type': 'multipart/form-data'
            }
        });

        // Show success message
        const html = `<div class="alert alert-success" role="alert">
        ${response.data.message}
        </div>`;
        message.innerHTML = html;

        // Reset form
        form.reset();

    } catch (error) {
        console.error("Error uploading attendance:", error);
        const html = `<div class="alert alert-danger" role="alert">
        ${error.response?.data?.message || "Failed to upload attendance. Please try again."}
        </div>`;
        message.innerHTML = html;
    }
});