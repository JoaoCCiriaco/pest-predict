document.addEventListener("DOMContentLoaded", function () {
    let button = document.getElementById("interestButton");

    if (button) {
        button.addEventListener("click", function () {
            document.getElementById("message").innerHTML =
                "Thanks for visiting my website!";
        });
    }

    let sendButton = document.getElementById("sendButton");

    if (sendButton) {
        sendButton.addEventListener("click", function () {
            document.getElementById("message").innerHTML =
                "Message received. Thank you!";
        });
    }
});
