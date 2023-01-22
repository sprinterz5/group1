
function setFormMessage(formElement, type, message) {
	const messageElement = formElement.querySelector(".form-message")
	messageElement.textContent = message
	messageElement.classList.remove("form-message-success", "form-message-error");
	messageElement.classList.add(`form-message-${type}`);
}

document.addEventListener("DOMContentLoaded", () => {
		const loginForm = document.querySelector("#login");
		loginForm.addEventListener("submit", e =>{
				e.preventDefault();
				// AJAX/Fetch login

				setFormMessage(loginForm,"error","Invalid username/password combination");
		});
});

const hamburger = document.querySelector(".hamburger")
const navMenu = document.querySelector(".nav-menu")
const exit = document.querySelector(".exit")
const card = document.querySelector(".main-card")
const assignments =document.querySelector(".assignments")
hamburger.addEventListener("click", () => {
	hamburger.classList.toggle("active");
	navMenu.classList.toggle("active");
});
exit.addEventListener("click", () => {
	hamburger.classList.remove("active");
	navMenu.classList.remove("active");
});
card.addEventListener("click", () => {
	assignments.classList.toggle("active");
});