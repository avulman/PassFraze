/*document.getElementById('generate').addEventListener('click', function() {
    window.location.href = '/generate';
});

document.getElementById('test').addEventListener('click', function() {
    window.location.href = '/test';
});

document.getElementById('crack').addEventListener('click', function() {
    window.location.href = '/crack';
});*/

document.getElementById('navigate_generate').addEventListener('click', function() {
    window.location.href = '/generate';
});

document.getElementById('navigate_test').addEventListener('click', function() {
    window.location.href = '/test';
});

document.getElementById('navigate_crack').addEventListener('click', function() {
    window.location.href = '/crack';
});

document.addEventListener("DOMContentLoaded", function() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(function(checkbox) {
        var checkboxId = checkbox.id;
        var storedValue = localStorage.getItem(checkboxId);
        if (storedValue !== null) {
            checkbox.checked = JSON.parse(storedValue);
        }
    });

    var lengthInput = document.getElementById('length');
    var storedLength = localStorage.getItem('passwordLength');
    if (storedLength !== null) {
        lengthInput.value = storedLength;
    }

    lengthInput.addEventListener('input', function() {
        var length = parseInt(this.value);
        if (length > 50) {
            length = 50;
            this.value = length;
        } else if (length < 1) {
            length = 1;
            this.value = length;
        }
        localStorage.setItem('passwordLength', length);
        updateGeneratedPassword();
    });
});

// Store checkbox states in localStorage when changed and submit the form
var checkboxes = document.querySelectorAll('input[type="checkbox"]');
checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        localStorage.setItem(this.id, this.checked);
        updateGeneratedPassword();
    });
});

function updateGeneratedPassword() {
    document.getElementById("passwordForm").submit();
}