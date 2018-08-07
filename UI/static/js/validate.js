/** 
 *  Handles the validation of input fields
 * 
* */


function getElement(element) {
    return document.getElementById(element);
}

function validateEmail(email) {
    if (email.validity.typeMismatch) {
        email.setCustomValidity("Valid email expected");
    } else {
        email.setCustomValidity("");
    }
}

function confirmPassword() {
    password = getElement("password").value;
    confirm_password = getElement("confirm-password").value;
    if (password != confirm_password) {
        confirm_password.setCustomValidity("Password does not match");
    }
    else {
        confirm_password.setCustomValidity("");
    }
}

email_input = getElement("email");
email_input.addEventListener("input", event => {
    validateEmail(email_input);
})



