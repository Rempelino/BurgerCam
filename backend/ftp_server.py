from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import tempfile
import time
import threading
import numpy as np
import cv2
from typing import Callable, Optional, Union
import logging


class FrameFTPServer:
    """
    An FTP server that serves a dynamically updated frame.
    The frame is updated when accessed by clients.
    """

    def __init__(self,
                 host: str = "0.0.0.0",
                 port: int = 2121,
                 username: str = "user",
                 password: str = "12345",
                 frame_filename: str = "current_frame.jpg",
                 frame_update_callback: Optional[Callable[[], Union[np.ndarray, None]]] = None):
        """
        Initialize the FTP server.

        Args:
            host: Host address to bind the server to
            port: Port to listen on
            username: FTP username for authentication
            password: FTP password for authentication
            frame_filename: Filename for the frame on the FTP server
            frame_update_callback: Callback function that returns a new frame when called
        """
        # Initialize attributes first to avoid errors in case of exceptions
        self.running = False

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("FrameFTPServer")

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.frame_filename = frame_filename
        self.frame_update_callback = frame_update_callback

        # Create a temporary directory to store the frame
        self.temp_dir = tempfile.mkdtemp()
        self.frame_path = os.path.join(self.temp_dir, self.frame_filename)

        # Create an initial empty frame if no callback is provided
        if self.frame_update_callback is None:
            empty_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.imwrite(self.frame_path, empty_frame)
        else:
            self._update_frame()

        # Set up authorizer and handlers
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user(username, password, self.temp_dir, perm="elradfmw")

        # Create custom handler with file download hook
        class FrameUpdateFTPHandler(FTPHandler):
            frame_server = self  # Reference to parent server

            def on_file_sent(self, file):
                # This method is called after a file download is complete
                if os.path.basename(file) == self.frame_server.frame_filename:
                    self.frame_server._update_frame()
                super().on_file_sent(file)

        self.handler = FrameUpdateFTPHandler
        self.handler.authorizer = self.authorizer

        # Set up server
        self.server = FTPServer((self.host, self.port), self.handler)
        self.server_thread = None

    def _update_frame(self):
        """Update the frame on disk using the callback function."""
        if self.frame_update_callback:
            frame = self.frame_update_callback()
            if frame is not None:
                cv2.imwrite(self.frame_path, frame)
                self.logger.info(f"Frame updated at {time.strftime('%H:%M:%S')}")

    def set_frame(self, frame: np.ndarray):
        """
        Manually set the current frame.

        Args:
            frame: NumPy array containing the image frame
        """
        cv2.imwrite(self.frame_path, frame)
        self.logger.info(f"Frame manually set at {time.strftime('%H:%M:%S')}")

    def set_frame_update_callback(self, callback: Callable[[], Union[np.ndarray, None]]):
        """
        Set or update the frame callback function.

        Args:
            callback: Function that returns a new frame when called
        """
        self.frame_update_callback = callback

    def start(self, blocking: bool = False):
        """
        Start the FTP server.

        Args:
            blocking: If True, blocks the current thread. If False, runs in a separate thread.
        """
        if self.running:
            self.logger.warning("Server is already running")
            return

        self.logger.info(f"Starting FTP server on {self.host}:{self.port}")
        self.logger.info(f"Serving frame at {self.frame_path}")
        self.logger.info(f"Username: {self.username}, Password: {self.password}")

        self.running = True

        if blocking:
            self.server.serve_forever()
        else:
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()

    def stop(self):
        """Stop the FTP server."""
        if not self.running:
            self.logger.warning("Server is not running")
            return

        self.logger.info("Stopping FTP server")
        self.server.close_all()
        self.running = False

        if self.server_thread:
            self.server_thread.join()

    def __del__(self):
        """Clean up resources when the object is deleted."""
        # Check if attributes exist to make the destructor more robust
        if hasattr(self, 'running') and self.running:
            self.stop()

        # Clean up the temporary directory
        if hasattr(self, 'temp_dir'):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                if hasattr(self, 'logger'):
                    self.logger.error(f"Error cleaning up temporary directory: {e}")
                else:
                    print(f"Error cleaning up temporary directory: {e}")


# Example usage
if __name__ == "__main__":
    # Define a callback function that generates a new frame
    def get_new_frame():
        # Create a simple test frame with timestamp
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (50, 240), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2, cv2.LINE_AA)
        return frame


    # Create and start the FTP server
    server = FrameFTPServer(
        host="0.0.0.0",  # Listen on all interfaces
        port=2121,
        username="user",
        password="12345",
        frame_filename="current_frame.jpg",
        frame_update_callback=get_new_frame
    )

    try:
        server.start(blocking=True)  # Run the server in the main thread
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop()