<p align="left">
  <img src="https://api.sadiq.workers.dev/app/github/repo/websocket-cam-streaming-server/views" alt="Repo views" />
</p>

# WebSocket Cam Streaming Server

A lightweight Python server for streaming live webcam video to a web browser using WebSockets and OpenCV. Includes basic HTTP authentication for secure access.

## Features

- Live video streaming from your webcam to a browser
- Uses WebSockets for efficient frame delivery
- Simple HTML frontend for viewing the stream
- Adjustable frame rate and quality
- Optional custom resolution support
- Basic HTTP authentication

## Requirements

- Python 3.7+
- [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
- [OpenCV (cv2)](https://opencv.org/)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sadiq-bd/websocket-cam-streaming-server.git
   cd websocket-cam-streaming-server
   ```

2. **Install dependencies:**
   ```bash
   pip install aiohttp opencv-python
   ```

## Usage

1. **Configure Settings:**

   Edit `main.py` to customize:
   - `STREAM_PORT`: Port number for the server (default: `7081`)
   - `STREAM_FPS`: Frames per second (default: `15`)
   - `STREAM_QUALITY`: JPEG quality (default: `50`)
   - `USERNAME` and `PASSWORD`: Credentials for basic authentication

   To set a custom resolution, uncomment and set `STREAM_RESOLUTION` (your camera must support it):
   ```python
   STREAM_RESOLUTION = "1280x720"  # Example resolution
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

3. **Access the stream:**

   Open your browser and go to:
   ```
   http://<server-ip>:7081/
   ```
   Replace `<server-ip>` with your server's IP address if running remotely.

4. **Authentication:**

   Enter the username and password you set in `main.py` when prompted.

## How It Works

- The server captures frames from your webcam using OpenCV.
- Each frame is encoded as a JPEG and sent to connected browsers over a WebSocket connection.
- The frontend page receives and displays frames in real time.
- Basic HTTP authentication is enforced for all routes.

## Security Note

- Credentials are hardcoded in `main.py` for demonstration. For production, use environment variables or a secure secrets manager.

## Troubleshooting

- **Webcam not detected:** Make sure your webcam is connected and accessible by OpenCV.
- **Port in use:** Change `STREAM_PORT` in `main.py` to an available port.
- **No video or broken stream:** Try a lower resolution or frame rate; check network/firewall settings.
- **Browser warnings:** The server does not use HTTPS by default; for public deployment, consider running behind a reverse proxy with SSL.

## License

MIT

## Credits

- [aiohttp](https://github.com/aio-libs/aiohttp)
- [OpenCV](https://github.com/opencv/opencv)
