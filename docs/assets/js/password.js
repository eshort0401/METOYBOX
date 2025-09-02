function checkPassword(targetPage) {
    const correctPassword = ""; // Change this to your desired password
    const userPassword = prompt("Enter password to access the model:");

    if (userPassword === correctPassword) {
        window.location.href = targetPage;
    } else if (userPassword !== null) { // User didn't cancel
        alert("Incorrect password. Access denied.");
    }
}
