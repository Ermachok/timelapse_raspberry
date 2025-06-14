import os
import threading

from picamera2 import Picamera2


class Camera:
    def __init__(self, save_dir):
        self.save_dir = save_dir
        self.lock = threading.Lock()
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())

    def take_photo(self, filename: str):
        with self.lock:
            path = os.path.join(self.save_dir, filename)
            self.picam2.capture_file(path)
        return filename
