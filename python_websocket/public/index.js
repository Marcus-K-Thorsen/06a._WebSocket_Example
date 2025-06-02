document.addEventListener("DOMContentLoaded", () => {
    const messageInput = document.getElementById("messageText");
    const messages = document.getElementById("messages");
    const currentUsername = document.getElementById("currentUserName");

    let ws;
    let isUsernameMissing = true;

    function connectWebSocket() {
        const wsUrl = "ws://localhost:8000/ws";
        ws = new WebSocket(wsUrl);

        // Handle incoming messages from the server
        ws.onmessage = function(event) {
            const message = document.createElement('li');
            const data = JSON.parse(event.data);
            // Update the current username display
            if (isUsernameMissing) {
                currentUsername.innerHTML = data.username;
                isUsernameMissing = false;
            }
            // Display the received message with the sender's username in bold
            const messageText = `<b>${data.username}:</b> ${data.message}`;
            message.innerHTML = messageText;
            messages.appendChild(message);
        };
    }

    // Establish the WebSocket connection when the DOM content is loaded
    connectWebSocket();

    // Handle form submission to send messages
    document.getElementById("chatForm").addEventListener("submit", (event) => {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            // Send the message to the server
            ws.send(message);
            messageInput.value = '';
        }
    });
});
