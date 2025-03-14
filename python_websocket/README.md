# Project Setup

## Initial Setup
```bash
 $ cd <project_directory>
 $ cd python_websocket
 $ poetry init --no-interaction
 $ poetry config virtualenvs.in-project true
 $ poetry add fastapi
 $ poetry add uvicorn
 $ poetry add jinja2
 $ poetry add websockets
 $ poetry add aiofiles
```

## Install
```bash
 $ cd <project_directory>
 $ cd python_websocket
 $ poetry config virtualenvs.in-project true
 $ poetry install --no-root
```

## Usage
```bash
 $ cd <project_directory>
 $ cd python_websocket
 $ poetry shell
 $ poetry run uvicorn main:app --reload
```


# Using the Chat App

1. **Start the Server:**
   - Ensure the server is running by executing the following command:
```bash
 $ poetry run uvicorn main:app --reload
```
   - The server will be running on `http://localhost:8000`.
2. **Open Multiple Connections:**
   - Open a web browser and navigate to `http://localhost:8000`.
   - This will open the chat app in your browser.
   - To simulate multiple users, open additional tabs or windows in the same browser and navigate to `http://localhost:8000` in each one.
   - Each tab or window will represent a different user in the chat app.
3. **Send and Receive Messages:**
   - In each tab or window, you can enter a message in the input field and click the "Send" button.
   - The message will be sent to the server and broadcast to all connected clients.
   - Each message will be displayed in the chat window with the sender's username in bold.
   - You can see messages from other users in real-time as they are sent.
4. **Disconnecting:**
   - If you close a tab or window, the server will detect the disconnection and broadcast a disconnection message to all remaining clients.
   - The remaining clients will see a message indicating that a user has disconnected.

This setup allows you to test the chat app with multiple users and see how messages are sent and received in real-time.
