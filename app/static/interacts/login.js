import {errorAlert} from "./error_alert.js"
window.onload = function() {
    let loginForm = document.getElementById('login-form');
    let registerFrom = document.getElementById('register-form');
    let toLogin = document.getElementById('to-login');
    let toRegister = document.getElementById('to-register');
    let toLoginBtn = document.getElementById('to-login-btn');
    let toRegisterBtn = document.getElementById('to-register-btn');

    toRegister.onclick = function() {
        loginForm.style.display = "none";
        toRegister.style.display = "none";
        registerFrom.style.display = "block";
        toLogin.style.display = "block";
    }
    toLogin.onclick = function() {
        registerFrom.style.display = "none";
        toLogin.style.display = "none";
        loginForm.style.display = "block";
        toRegister.style.display = "block";
    }
    errorAlert();
}
