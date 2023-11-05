const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const axios = require('axios'); // Make sure to import axios

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static('.'));

io.on('connection', (socket) => {
    console.log('a user connected');
    
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
    
    socket.on('message', async (msg) => {
        try {
            const response = await axios.post('http://localhost:5000/generate', {
                prompt: msg
            });

            const botResponse = response.data;
            io.emit('message', { user: 'bot', ...botResponse });
        } catch (error) {
            console.error('Error connecting to Python server:', error);
        }
    });
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});
