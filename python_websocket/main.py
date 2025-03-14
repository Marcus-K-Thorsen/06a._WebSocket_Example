from fastapi import (
    FastAPI,
    WebSocket, 
    WebSocketDisconnect
    )
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2.environment import Template
from connection_manager import ConnectionManager

app = FastAPI()
app.mount("/static", StaticFiles(directory="public"), name="static")

connection_manager = ConnectionManager()
root_page: Template = Jinja2Templates(directory="public").get_template("index.html")


@app.get("/")
async def serve_root_page():
    return HTMLResponse(root_page.render())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection
    await connection_manager.connect(websocket)
    try:
        while True:
            # Receive a message from the client
            data = await websocket.receive_text()
            # Broadcast the message to all connected clients
            await connection_manager.broadcast(websocket, message=data)
    except WebSocketDisconnect:
        # Handle WebSocket disconnection
        websocket_data = connection_manager.disconnect(websocket)
        # Broadcast a disconnection message to all connected clients
        await connection_manager.broadcast(websocket_data, message="Disconnected")
        