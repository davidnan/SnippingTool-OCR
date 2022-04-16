import mss
from PIL import Image

class PrintScreen():
    def __init__(self, image_path, focused_monitor):
        self.image_path = image_path
        self.focused_monitor = focused_monitor + 1

    def take_screenshot(self):
        with mss.mss() as mss_instance:
            self.m = mss_instance.monitors[self.focused_monitor]
            self.ss = mss_instance.grab(self.m)
            img = Image.frombytes("RGB", self.ss.size, self.ss.bgra, "raw", "BGRX")  # Convert to PIL.Image
            img.save(self.image_path, 'PNG')