document.getElementById("passwordForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    var website = document.getElementById("website").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    
    // Send data to backend
    fetch("/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({website: website, username: username, password: password})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById("passwordForm").reset();
        getPasswords();
    })
    .catch(error => console.error("Error:", error));
});

function getPasswords() {
    fetch("/get")
    .then(response => response.json())
    .then(data => {
        console.log(data);
        var passwordContainer = document.getElementById("passwordContainer");
        passwordContainer.innerHTML = "";
        data.forEach(function(password) {
            var passwordElement = document.createElement("div");
            passwordElement.textContent = password.website + " - " + password.username;
            passwordContainer.appendChild(passwordElement);
        });
    })
    .catch(error => console.error("Error:", error));
}

getPasswords();
