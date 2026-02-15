const first_name = document.querySelector("#first_name");
const middle_name = document.querySelector("#middle_name");
const last_name = document.querySelector("#last_name");
const date_of_birth = document.querySelector("#date_of_birth");
const genders = document.querySelectorAll('input[name="gender"]');
const email = document.querySelector("#email");
const password = document.querySelector("#password");
const confirm_password = document.querySelector("#confirm_password");
const contact_number = document.querySelector("#contact_number");
const address_line_1 = document.querySelector("#address_line_1");
const address_line_2 = document.querySelector("#address_line_2");
const landmark = document.querySelector("#landmark");
const pincode = document.querySelector("#pincode");
const state = document.querySelector("#state");
const city = document.querySelector("#city");
const college = document.querySelector("#college");
const role = document.querySelector("#role");
const submit = document.querySelector("#submit");
const message = document.querySelector("#message");

// Add a new function to validate all required fields
function validateRequiredFields() {
    let isValid = true;
    let errorMessage = '';
    
    // Check required text fields
    const requiredFields = [
        { element: first_name, name: 'First Name' },
        { element: last_name, name: 'Last Name' },
        { element: date_of_birth, name: 'Date of Birth' },
        { element: email, name: 'Email' },
        { element: password, name: 'Password' },
        { element: confirm_password, name: 'Confirm Password' },
        { element: contact_number, name: 'Contact Number' },
        { element: address_line_1, name: 'Address Line 1' },
        { element: address_line_2, name: 'Address Line 2' },
        { element: landmark, name: 'Landmark' },
        { element: pincode, name: 'Pincode' }
    ];
    
    for (const field of requiredFields) {
        if (!field.element.value.trim()) {
            field.element.classList.add('error');
            isValid = false;
            errorMessage += `${field.name} is required.<br>`;
        } else {
            field.element.classList.remove('error');
        }
    }
    
    // Check dropdown fields
    const dropdowns = [
        { element: state, name: 'State' },
        { element: city, name: 'City' },
        { element: college, name: 'College' },
        { element: role, name: 'Role' }
    ];
    
    for (const dropdown of dropdowns) {
        if (!dropdown.element.value) {
            dropdown.element.classList.add('error');
            isValid = false;
            errorMessage += `Please select a ${dropdown.name}.<br>`;
        } else {
            dropdown.element.classList.remove('error');
        }
    }
    
    // Check gender radio buttons
    let genderSelected = false;
    for (const gender of genders) {
        if (gender.checked) {
            genderSelected = true;
            break;
        }
    }
    
    if (!genderSelected) {
        document.getElementById('radio-button').classList.add('error');
        isValid = false;
        errorMessage += 'Please select a Gender.<br>';
    } else {
        document.getElementById('radio-button').classList.remove('error');
    }
    
    // Display error message if validation fails
    if (!isValid) {
        message.innerHTML = `<div class="alert alert-danger" role="alert">${errorMessage}</div>`;
    }
    
    return isValid;
}

function matchPassword(event) {
    if (password.value != confirm_password.value) {
        document.querySelector(".pass").classList.add("error")
        document.querySelector(".cf").classList.add("error")
        message.innerHTML = '<div class="alert alert-danger" role="alert">Password and Confirm Password do not match!</div>';
        return false;
    }
    else {
        document.querySelector(".pass").classList.remove("error")
        document.querySelector(".cf").classList.remove("error")
        message.innerHTML = '';
        return true;
    }
}

async function register(event) {
    event.preventDefault();
    try {
        // First validate all required fields
        if (!validateRequiredFields()) {
            return; // Stop form submission if validation fails
        }
        
        // Check if passwords match before proceeding
        if (!matchPassword()) {
            return;  // Stop form submission if passwords don't match
        }
        
        let selectedGender = ""
        for (const gendar of genders) {
            if (gendar.checked) {
                selectedGender = gendar.value;
                break;
            }
        }
        
        payload = {
            first_name: first_name.value,
            middle_name: middle_name.value,
            last_name: last_name.value,
            date_of_birth: date_of_birth.value,
            email: email.value,
            password: password.value,
            gender: selectedGender,
            contact_number: contact_number.value,
            address_line_1: address_line_1.value,
            address_line_2: address_line_2.value,
            landmark: landmark.value,
            pincode: pincode.value,
            state: state.value,
            city: city.value,
            college: college.value,
            role: role.value
        }
        console.log(payload)
        let register_info = await axios({
            method: "POST",
            url: "http://localhost:8000/signup/",
            data: payload
        })
        console.log(register_info)
        const html = `<div class="alert alert-success" role="alert">
        User Registered
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
        setTimeout(redirect,500);
    } catch (error) {
        console.log(error)
        const html = `<div class="alert alert-primary" role="alert">
        <span id = "message" style="color:red">${error.response.data.message}</span>
        </div>`
        message.innerHTML = ""
        message.insertAdjacentHTML("beforeend", html)
    }

}

function redirect() {
    window.location.href = `/login.html`
}

confirm_password.addEventListener("input", matchPassword)
submit.addEventListener("click", register)