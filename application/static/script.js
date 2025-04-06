const showRegisterPopup = document.querySelector(".login-btn");

showRegisterPopup.addEventListener("click", () => {
    document.body.classList.toggle("show-popup");
});

// Show Register Form Popup
const hideRegisterPopup = document.querySelector(".form-popup .close-btn");

// Hide Register Form Popup
hideRegisterPopup.addEventListener("click", () => showRegisterPopup.click());