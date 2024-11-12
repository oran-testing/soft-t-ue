const express = require('express');
const WebSocket = require('ws');
const app = express();
const port = 3000;

// Track UE WebSocket clients and port range
const ueWsClients = {};
const localhostPortRange = { start: 8765, end: 8865 };

// Serve static files (HTML, CSS, JS)
app.use(express.static('public'));

// WebSocket server to broadcast UE logs to frontend clients
const server = app.listen(port, () => {
    console.log(`Express server running on http://localhost:${port}`);
});

const wss = new WebSocket.Server({ server });
wss.on('connection', (ws) => {
    console.log("Client connected to Node.js WebSocket");

    // On receiving a message, broadcast logs from UEs to all clients
    Object.keys(ueWsClients).forEach(ueKey => {
        ueWsClients[ueKey].on('message', (message) => {
            console.log(message);
            ws.send(JSON.stringify({ ueId: ueKey, log: message }));
        });
    });

    ws.on('close', () => {
        console.log("Client disconnected from Node.js WebSocket");
    });
});

// Scan the localhost port range for available WebSocket servers
async function scanLocalhostPorts() {
    for (let port = localhostPortRange.start; port <= localhostPortRange.end; port++) {
        const url = `ws://localhost:${port}`;
        const ueKey = `UE-${port}`;

        try {
            // Attempt to connect to each port in the range
            const ueWs = new WebSocket(url);

            ueWs.on('open', () => {
                console.log(`Connected to WebSocket at ${url}`);
                ueWsClients[ueKey] = ueWs; // Store connection on success
            });

            ueWs.on('message', (message) => {
                // Broadcast each log message to all connected clients
                wss.clients.forEach(client => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify({ ueId: ueKey, log: message }));
                    }
                });
            });

            ueWs.on('close', () => {
                console.log(`${ueKey} WebSocket closed`);
                delete ueWsClients[ueKey];
            });

            ueWs.on('error', (error) => {
                console.log(`Failed to connect to WebSocket at ${url}: ${error.message}`);
            });
        } catch (error) {
            console.log(`Error connecting to ${url}: ${error.message}`);
        }
    }
}

scanLocalhostPorts();

