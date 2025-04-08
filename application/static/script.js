
// Useful Browser Events:
// "click"        mouse click
// "dblclick"     double click
// "keydown"      key pressed
// "keyup"        key released
// "scroll"       user scrolls
// "input"        user types into input
// "submit"       form is submitted


// Show Register Form Popup when 'As a Client' button is clicked.
const showRegisterPopup = document.querySelector(".login-btn");

showRegisterPopup.addEventListener("click", function() {
    document.body.classList.toggle("show-popup");
});

// Hide Register Form Popup when the 'x' icon is clicked.
const hideRegisterPopup = document.querySelector(".form-popup .close-btn");

hideRegisterPopup.addEventListener("click", function() {showRegisterPopup.click()});


// Make labels disappear when the user types in the input field.
const textbox = document.getElementsByClassName('.input-field')
const label = document.getElementById('label')

const loginButtons = document.querySelectorAll(".login-btn");

