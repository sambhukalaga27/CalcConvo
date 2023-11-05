const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const axios = require('axios'); // Make sure to import axios

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static('.'));

const PORT = process.env.PORT //|| 3000; // Use environment variable for port
const PYTHON_SERVER_URL = process.env.PYTHON_SERVER_URL // || 'http://localhost:5000'; // Use environment variable for Python server URL

io.on('connection', (socket) => {
    console.log('a user connected');
    
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
    
    socket.on('message', async (msg) => {
        try {
            const response = await axios.post(`${PYTHON_SERVER_URL}/generate`, {
                prompt: msg
            });

            const botResponse = response.data;
            io.emit('message', { user: 'bot', ...botResponse });
        } catch (error) {
            console.error('Error connecting to Python server:', error);
        }
    });
});

server.listen(PORT, () => {
    console.log(`listening on *:${PORT}`);
});
