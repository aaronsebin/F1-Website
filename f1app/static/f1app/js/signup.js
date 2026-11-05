
const signupForm = document.getElementById("signupForm");

const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm_password");

const usernameError = document.getElementById("usernameError");
const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");
const confirmPasswordError = document.getElementById("confirmPasswordError");


// Display an error message for a field
function showError(input, errorElement, message) {
    errorElement.textContent = message;
    input.classList.add("invalid");
    input.classList.remove("valid");
}


// Clear the error message for a field
function clearError(input, errorElement) {
    errorElement.textContent = "";
    input.classList.remove("invalid");
}


// Clear all validation messages
function clearAllErrors() {
    clearError(username, usernameError);
    clearError(email, emailError);
    clearError(password, passwordError);
    clearError(confirmPassword, confirmPasswordError);
}


// Validate username
function validateUsername() {

    const value = username.value.trim();

    if (value === "") {
        showError(
            username,
            usernameError,
            "Username is required."
        );

        return false;
    }

    if (value.length < 3) {
        showError(
            username,
            usernameError,
            "Username must be at least 3 characters long."
        );

        return false;
    }

    clearError(username, usernameError);
    username.classList.add("valid");

    return true;
}


// Validate email
function validateEmail() {

    const value = email.value.trim();

    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (value === "") {
        showError(
            email,
            emailError,
            "Email address is required."
        );

        return false;
    }

    if (!emailPattern.test(value)) {
        showError(
            email,
            emailError,
            "Please enter a valid email address."
        );

        return false;
    }

    clearError(email, emailError);
    email.classList.add("valid");

    return true;
}


// Validate password
function validatePassword() {

    const value = password.value;

    if (value === "") {
        showError(
            password,
            passwordError,
            "Password is required."
        );

        return false;
    }

    if (value.length < 6) {
        showError(
            password,
            passwordError,
            "Password must be at least 6 characters long."
        );

        return false;
    }

    clearError(password, passwordError);
    password.classList.add("valid");

    return true;
}


// Validate confirm password
function validateConfirmPassword() {

    const value = confirmPassword.value;

    if (value === "") {
        showError(
            confirmPassword,
            confirmPasswordError,
            "Please confirm your password."
        );

        return false;
    }

    if (value !== password.value) {
        showError(
            confirmPassword,
            confirmPasswordError,
            "Passwords do not match."
        );

        return false;
    }

    clearError(confirmPassword, confirmPasswordError);
    confirmPassword.classList.add("valid");

    return true;
}


// Validate the complete signup form
signupForm.addEventListener("submit", function(event) {

    clearAllErrors();

    const usernameValid = validateUsername();
    const emailValid = validateEmail();
    const passwordValid = validatePassword();
    const confirmPasswordValid = validateConfirmPassword();

    const formIsValid =
        usernameValid &&
        emailValid &&
        passwordValid &&
        confirmPasswordValid;

    if (!formIsValid) {

        event.preventDefault();

        // Focus the first invalid field
        const firstInvalidField =
            signupForm.querySelector(".invalid");

        if (firstInvalidField) {
            firstInvalidField.focus();
        }
    }

});


// Validate fields when the user leaves them
username.addEventListener("blur", validateUsername);
email.addEventListener("blur", validateEmail);
password.addEventListener("blur", validatePassword);
confirmPassword.addEventListener("blur", validateConfirmPassword);


// Recheck password confirmation when the password changes
password.addEventListener("input", function() {

    if (confirmPassword.value !== "") {
        validateConfirmPassword();
    }

});
