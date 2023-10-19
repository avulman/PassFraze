function generatePassword() {
    eel.generate_password()();
}

function testPasswordStrength() {
    eel.test_own_password()();
}

function crackPassword() {
    eel.crack_password()();
}

eel.expose(updateCurrentPassword);

function updateCurrentPassword(password) {
    const currentPasswordElement = document.getElementById('current-password');
    currentPasswordElement.innerText = password;
}