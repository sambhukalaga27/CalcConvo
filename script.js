const socket = io();
const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const graphBox = document.getElementById('graph-box');

function sendMessage() {
    const message = chatInput.value.trim();
    if (message) {
        socket.emit('message', message);
        displayMessage('You', message); // Display user's message
        chatInput.value = '';
    }
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

socket.on('message', (message) => {
    if (message.user === 'bot') {
        if (message.plot_data) {
            // If there's plot data, display the plot using Plotly
            displayPlot(message.plot_data);
        } else {
            const botMessage = message.text; // Make sure 'text' is the correct property
            displayMessage('Bot', botMessage); // Display bot's message
        }
    }
});

function displayMessage(sender, message) {
    const msgElement = document.createElement('div');
    msgElement.classList.add('message');
    if (sender === 'You') {
        msgElement.classList.add('user-message');
    } else {
        msgElement.classList.add('bot-message');
    }
    msgElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(msgElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

function displayPlot(plotData) {
    console.log("Received plot data:", plotData);
    Plotly.newPlot('graph-box', JSON.parse(plotData));
}
