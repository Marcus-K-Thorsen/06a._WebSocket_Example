from fastapi import WebSocket
from pydantic import BaseModel, ConfigDict
from typing import Optional, Union

    

class WebSocketData(BaseModel):
    message: str 
    username: str
    
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    
class WebSocketConnection(BaseModel):
    websocket: WebSocket
    username: str
    
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocketConnection] = []
        self.connection_count: int = 0
    
    async def connect(self, websocket: WebSocket):
        # IMPORTANT: Accept the WebSocket connection
        await websocket.accept()
        # Increment the connection count and generate a unique username
        self.connection_count += 1
        new_websocket_connection_username = f"User {self.connection_count}"
        # Create a new WebSocketConnection object
        websocket_connection = WebSocketConnection(
            websocket=websocket, 
            username=new_websocket_connection_username
            )
        # Add the new connection to the list of active connections
        self.active_connections.append(websocket_connection)
    
    def disconnect(self, websocket: WebSocket) -> WebSocketData:
        # Find the connection to disconnect
        found_connection = self.find_connection(websocket)
        if found_connection:
            # Remove the connection from the list of active connections
            self.active_connections.remove(found_connection)
            # Return a WebSocketData object indicating disconnection
            return WebSocketData(
                message="Disconnected",
                username=found_connection.username
            )
        # Return a WebSocketData object indicating client not found
        return WebSocketData(
            message="Client not found",
            username="System"
        )
        
    async def send(self, websocket: WebSocket, message: str):
        # Find the connection to send the message to
        found_connection = self.find_connection(websocket)
        if found_connection:
            # Send the message as a JSON object
            await websocket.send_json(
                WebSocketData(
                    message=message,
                    username=found_connection.username
                ).model_dump()
            )
    
    def find_connection(self, websocket: WebSocket) -> Optional[WebSocketConnection]:
        # Find and return the connection matching the given WebSocket
        for connection in self.active_connections:
            if connection.websocket == websocket:
                return connection
        return None
        
    async def broadcast(self, websocket: Union[WebSocket, WebSocketData], message: str):
        if isinstance(websocket, WebSocket):
            # Find the connection to broadcast the message from
            found_connection = self.find_connection(websocket)
            sender = "System" if found_connection is None else found_connection.username
            message = "Client not found" if found_connection is None else message
            
            # Create a WebSocketData object for the message
            web_socket_data = WebSocketData(
                message=message,
                username=sender
            )
            
        else:
            web_socket_data = websocket
        
        # Convert the WebSocketData object to a dictionary
        data = web_socket_data.model_dump()
        
        # Send the message to all active connections
        for connection in self.active_connections:
            await connection.websocket.send_json(data)
        