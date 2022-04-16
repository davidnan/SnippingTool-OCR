import pyautogui
import os, sys
from screeninfo import get_monitors
from PIL import Image, ImageTk
import tkinter as tk
from snippingtool.cutPrintScreen import CutPS
from snippingtool.printScreen import PrintScreen
from snippingtool.monitors import Monitors
from PyQt5.Qt import QApplication

class SnippingTool():
    app: QApplication
    cutPs: CutPS

    def __init__(self) -> None:
        self.local_path = os.path.abspath(os.getcwd())
        self.image_path = self.local_path + "\img.png"
        self.monitors = Monitors()
        self.ss = PrintScreen(self.image_path, self.monitors.focused_monitor)

    def initCutPS(self):
        self.app = QApplication(sys.argv)
        self.cutPs = CutPS(self.image_path, self.monitors.focused_monitor, self.monitors.res)
        self.cutPs.setApp(self.app)
        self.cutPs.show()

    def __del__(self):
        if os.path.exists(self.image_path):
            # os.remove(self.image_path)
            pass



if __name__ == "__main__":
    ps = SnippingTool()
    ps.ss.take_screenshot()
    ps.initCutPS()
    sys.exit(ps.app.exec_())


