import base64
import cv2
import time
from aiohttp import web

STREAM_PORT = 7081
STREAM_FPS = 20

# Hardcoded credentials (change these to your desired username and password)
USERNAME = "admin"
PASSWORD = "123"



# HTML content for the video stream page 
stream_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cam Video Stream</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #000;
        }

        #video {
            border: 2px solid #333;
            margin: 20px;
            width: 100%;
            max-width: 720px;
            height: auto;
        }

        @media (max-width: 600px) {
            #video {
                width: 100%;
                height: auto;
            }
        }
    </style>
</head>
<body>
    <img id="video" />
    <script>
        // Automatically detect WebSocket host from the current HTTP host
        const wsProto = window.location.protocol.toLowerCase() == 'https:' ? 'wss' : 'ws'; 
        const wsHost = window.location.hostname;
        const wsPort = window.location.port;
        const wsUrl = `${wsProto}://${wsHost}:${wsPort}/stream`;

        const videoElement = document.getElementById("video");
        const ws = new WebSocket(wsUrl);

        ws.binaryType = "blob"; // Make sure to receive binary data

        ws.onmessage = function(event) {
            const blob = event.data;
            videoElement.src = URL.createObjectURL(blob);
        };

        ws.onclose = function() {
            alert("Connection closed");
        };
    </script>
</body>
</html>"""

# WebSocket handler for video streaming
async def stream_video(request):
    """Stream live video data from the webcam to the WebSocket client."""
    print("Browser connected for streaming.")
    
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    # Open the default webcam
    cap = cv2.VideoCapture(0)  # 0 is the default webcam
    if not cap.isOpened():
        print("Error: Cannot access the webcam.")
        return ws

    try:
        while True:
            # Capture a frame from the webcam
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame. Exiting.")
                break

            # Encode the frame as a JPEG image
            _, buffer = cv2.imencode('.jpg', frame)
            data = buffer.tobytes()

            # Send the frame as binary data to the WebSocket client
            await ws.send_bytes(data)
            print(f"Sent frame of size {len(data)} bytes.")

            # Control the frame rate (adjust for desired FPS)
            time.sleep(1 / STREAM_FPS)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Release the webcam resource
        cap.release()
        print("WebSocket connection closed and webcam released.")
        await ws.close()
    
    return ws

# Basic Auth helper function to validate credentials
def check_basic_auth(request: web.Request):
    auth = request.headers.get('Authorization')
    if auth is None:
        return False

    # Extract base64 encoded username:password
    auth_type, auth_str = auth.split(' ', 1)
    if auth_type.lower() != 'basic':
        return False

    # Decode the base64 string
    try:
        decoded = base64.b64decode(auth_str).decode('utf-8')
        username, password = decoded.split(":", 1)
    except Exception:
        return False

    # Compare with hardcoded credentials
    return username == USERNAME and password == PASSWORD

# Middleware to handle basic authentication
@web.middleware
async def auth_middleware(request, handler):
    # if request.path == "/stream":
    if not check_basic_auth(request):
        # If no auth or wrong auth, return 401 Unauthorized
        return web.Response(
            status=401,
            headers={"WWW-Authenticate": "Basic realm='Login required'"},
            text="Unauthorized"
        )
    return await handler(request)

# Application setup and routes
app = web.Application(middlewares=[auth_middleware])

# HTTP routes
app.router.add_get('/', lambda request: web.Response(content_type='text/html', text=stream_html))
app.router.add_get('/stream', stream_video)

# Start the server on the same port 
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=STREAM_PORT)
