import pyautogui
from PIL import Image
import os
import cv2

class PrintScreen():
    def __init__(self) -> None:
        self.ph = pyautogui.screenshot()
        self.local_path = os.path.abspath(os.getcwd())
        self.image_path = self.local_path + "img.png"

    def save_screenshot(self) -> None:
        self.ph.save(self.image_path)

    def open_image(self) -> None:
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("window", self.image_path)
        
if __name__ == "__main__":
    ps = PrintScreen()
    ps.save_screenshot()
    ps.open_image()
       
