
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

// Make labels disappear when the user types in the input field.
const inputBox = document.getElementsByClassName('.input-field');
const label = document.getElementById('label');

function removeTheLabel() {
    inputBox.classList.remove(label);
}
inputBox.addEventListener("keydown", removeTheLabel());

// Trigger the typing animation on the about section when user is within viewport of the about section.
// const typingAnimation = document.querySelector(".typing-text")
// const aboutSection = document.getElementById("about-section")

// window.addEventListener("scroll", function() {
//     const position = aboutSection.getBoundingClientRect()

//     if (position.top <= window.innerHeight * 0.5 && position.bottom >= window.innerHeight * 0.5 ) {
//         typingAnimation.classList.add("start-typing");
//     } else {
//         typingAnimation.classList.remove("start-typing");
//     }
// });


// const topPosition = aboutSection.offsetTop;

// function triggerTyping() {
//     if (window.scrollY >= topPosition) {
//         typingAnimation.classList.add("start-typing");
//     } else {
//         typingAnimation.classList.remove("start-typing");
//     }
// }
// window.addEventListener("scroll", triggerTyping());

// .typing-text.start-typing .line-1,
// .typing-text.start-typing .line-2 {
//     visibility: visible;
// } 

AOS.init({
    duration: 800,
    easing: 'ease-in-out',
  });