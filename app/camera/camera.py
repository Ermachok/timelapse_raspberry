import os
import uuid

from picamera2 import Picamera2


class Camera:
    def __init__(self, save_dir: str):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())

    def take_photo(self) -> str:
        filename = f"{uuid.uuid4()}.jpg"
        path = os.path.join(self.save_dir, filename)
        self.picam2.start()
        self.picam2.capture_file(path)
        self.picam2.stop()
        return filename
