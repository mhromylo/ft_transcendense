const API_BASE_URL = "http://localhost:8000/api/accounts/";

async function registerUser() {
    const username = document.getElementById("register-username").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value.trim();

    if (!username || !email || !password) {
        alert("All fields are required!");
        return;
    }

    try {
        const response = await fetch(API_BASE_URL + "register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, email, password }),
        });

        if (response.ok) {
            alert("Registration successful!");
        } else {
            const errorData = await response.json();
            alert("Error: " + JSON.stringify(errorData));
        }
    } catch (error) {
        alert("An unexpected error occurred: " + error.message);
    }
}


async function loginUser() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch(API_BASE_URL + "login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        document.getElementById("login-form").style.display = "none";
        document.getElementById("user-info").style.display = "block";
        document.getElementById("username").innerText = username;
    } else {
        alert("Invalid credentials.");
    }
}

function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    document.getElementById("user-info").style.display = "none";
    document.getElementById("login-form").style.display = "block";
}
