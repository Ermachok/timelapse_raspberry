import os
import subprocess
import threading
import time
from typing import Optional

from camera.camera import Camera


class TimelapseController:
    def __init__(self, camera: Camera, interval: float = 5.0):
        self.camera = camera
        self.interval = interval
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.latest_photo: Optional[str] = None
        self.frame_counter = 0
        self.video_path = os.path.join(self.camera.save_dir, "timelapse.mp4")

    def start(self):
        if not self.running:
            self.running = True
            self.frame_counter = 0
            self._cleanup_photos()
            self.thread = threading.Thread(target=self._worker, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.create_timelapse_video()

    def _worker(self):
        with self.camera.lock:
            self.camera.picam2.start()
            try:
                while self.running:
                    filename = f"frame_{self.frame_counter:04d}.jpg"
                    self.camera.take_photo(filename)
                    self.latest_photo = filename
                    self.frame_counter += 1
                    time.sleep(self.interval)
            finally:
                self.camera.picam2.stop()

    def get_latest_photo_path(self) -> Optional[str]:
        if self.latest_photo:
            return os.path.join(self.camera.save_dir, self.latest_photo)
        return None

    def get_video_path(self) -> Optional[str]:
        return self.video_path if os.path.exists(self.video_path) else None

    def create_timelapse_video(self):
        cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            "5",
            "-i",
            os.path.join(self.camera.save_dir, "frame_%04d.jpg"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            self.video_path,
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при сборке видео: {e}")

    def _cleanup_photos(self):
        for file in os.listdir(self.camera.save_dir):
            if file.startswith("frame_") and file.endswith(".jpg"):
                os.remove(os.path.join(self.camera.save_dir, file))
