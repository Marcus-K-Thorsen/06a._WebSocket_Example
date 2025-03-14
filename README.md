# 06a [Individual] WebSocket Example

**Type**: Individual

Have a simple web socket example. 



# WebSocket

WebSocket is a communication protocol that provides full-duplex communication channels over a single TCP connection.

Defined by [RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)



---

# WebSocket vs. HTTP

* HTTP is built on top of TCP.
* WebSocket is built on top of TCP.
* WebSocket is a separate protocol from HTTP but it starts with an HTTP handshake to establish the connection. Then it switches to the WebSocket protocol.
* WebSockets are bidirectional. Use SSE when you want the server to update the client but don’t want to receive anything from clients.
* WebSockets can transmit both binary data and UTF-8. SSE only UTF-8.

---

# Real-time communication

Many resources define WebSocket as a protocol for real-time communication.

**Isn't HTTP just as "real-time"? What does it even mean to be real-time?**

It doesn't have a clear definition and doesn't convey much information.

Being "real-time" is not a defining characteristic of WebSockets, as SSE and HTTP long-polling can achieve the same result.

But most resources sell WebSocket as a real-time protocol and it is often the first thing they mention.

### [Wikipedia](https://en.wikipedia.org/wiki/Real-time_computing) defines three categories of **real-time constraints**:

#### Hard
- Missing a deadline is a total system failure.
- Car engine control systems, medical systems (pacemakers), industrial process controllers (assembly line).

#### Firm
- Infrequent deadline misses are tolerable, but may degrade the system's quality of service. The usefulness of a result is zero after its deadline.
- What fits here can be argued about.

#### Soft
- The usefulness of a result degrades after its deadline, thereby degrading the system's quality of service.
- Video streaming. Online gaming.

---

## Understanding WebSockets

WebSockets provide a full-duplex communication channel over a single TCP connection, allowing for real-time data exchange between the client and server.

### How WebSockets Work

1. **Client Initiates WebSocket Connection**:
    - The client initiates a WebSocket connection by sending an HTTP request with an `Upgrade` header to the server.
    - This request is typically made using the `WebSocket` API in JavaScript.
    - This can be seen in the `index.js` file: In this code, the `connectWebSocket` function is called when the DOM content is loaded, and it initiates the `WebSocket` connection by creating a new WebSocket object with the URL `ws://localhost:8000/ws`.

```javascript
function connectWebSocket() {
    const wsUrl = "ws://localhost:8000/ws";
    ws = new WebSocket(wsUrl);
    ws.onmessage = function(event) {
        const message = document.createElement('li');
        const data = JSON.parse(event.data);
        const messageText = `<b>${data.sender}</b>: ${data.message}`;
        message.innerHTML = messageText;
        messages.appendChild(message);
    };
}
```

2. **Server Accepts WebSocket Connection**:
    - The server responds to the `Upgrade` request by switching the protocol from HTTP to WebSocket.
    - Once the connection is established, both the client and server can send and receive messages at any time.
    - This can be seen in the `main.py` file: In this code, specifically in the websocket_endpoint function where the server accepts the WebSocket connection and handles incoming messages:
      - The server accepts the WebSocket connection when the connect method of the ConnectionManager is called.
      - The server then enters a loop to receive and broadcast messages.
      - If the WebSocket disconnects, the server handles the disconnection and broadcasts a disconnection message.



```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    username = await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(message=data, sender=username)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(message="Client disconnected", sender=username)
```

3. **Full-Duplex Communication**:
    - The WebSocket connection remains open, allowing for continuous, bidirectional communication.
    - Both the client and server can send messages to each other without the need to re-establish the connection.
    - **Client-Side Code**:
    	- In the `index.js` file, the WebSocket connection remains open, and the client can send messages to the server and receive messages from the server.
    	- Here is the relevant part of the `index.js` file:
    	- The WebSocket connection is established and remains open.
    	- The client can send messages to the server using ws.send(message).
    	- The client can receive messages from the server using ws.onmessage.

```javascript
ws.onmessage = function(event) {
    // Code for what happens on a message being recieved
    };
```

```javascript
ws.send(message);
```



   - **Server-side Code**:
     -  In the main.py file, the server can receive messages from the client and broadcast messages to all connected clients.
     -  Here is the relevant part of the main.py file:
     -  The WebSocket connection remains open, allowing the server to continuously receive and send messages.
     -  The server can receive messages from the client using 
     `await websocket.receive_text()`.
     -  The server can broadcast messages to all connected clients using 
     `await connection_manager.broadcast(message=data, sender=username)`.

```python
data = await websocket.receive_text()
```
```python
await connection_manager.broadcast(message="Client disconnected", sender=username)
```

### Illustration

```plaintext
+---------+            +---------+
|  Client |            |  Server |
+---------+            +---------+
     |                      |
     |  WebSocket Handshake |
     |--------------------->|
     |                      |
     |  Protocol Upgrade    |
     |<---------------------|
     |                      |
     |  Send Message        |
     |<-------------------->|
     |                      |
     |  Receive Message     |
     |<-------------------->|
     |                      |
     |  Close Connection    |
     |<-------------------->|
     |                      |
```

In this illustration:

* The client initiates a WebSocket handshake with the server.
* The server responds by upgrading the protocol to WebSocket.
* Both the client and server can send and receive messages over the open
  connection.
* The connection remains open until either the client or server decides to
  close it.


In the context of the chat app:

- When a client connects, they are assigned a unique username by the server.
- The client can send messages to the server, which are then broadcast to all connected clients.
- Each message includes the sender's username, which is displayed in bold.
- If a client disconnects, the server broadcasts a disconnection message to all remaining clients.
- This allows all clients to see messages from other clients in real-time, maintaining an open and continuous communication channel.