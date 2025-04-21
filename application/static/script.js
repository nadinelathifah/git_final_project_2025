
// Useful Browser Events:
// "click"        mouse click
// "dblclick"     double click
// "keydown"      key pressed
// "keyup"        key released
// "scroll"       user scrolls
// "input"        user types into input
// "submit"       form is submitted


// Show the popup Client login form
const clientForm = document.getElementById("client-login");
const clientButton = document.querySelector(".login-btn.client");
clientButton.addEventListener("click", function() {
    document.body.classList.add("show-popup");
    clientForm.classList.add("show-popup");
});

// Show the popup Tradesperson login form
const tradespersonForm = document.getElementById("tradesperson-login");
const tradespersonButton = document.querySelector(".login-btn.tradesperson");
tradespersonButton.addEventListener("click", function() {
    document.body.classList.add("show-popup");
    tradespersonForm.classList.add("show-popup");
});

// Close both forms
const closeForms = document.querySelectorAll(".form-popup .close-btn").forEach(function(button) {
    button.addEventListener("click", function() {
        document.body.classList.remove("show-popup");
        clientForm.classList.remove("show-popup");
        tradespersonForm.classList.remove("show-popup");
    });
});


AOS.init({
    duration: 800,
    easing: 'ease-in-out',
  });