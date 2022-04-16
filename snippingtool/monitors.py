from screeninfo import get_monitors
import pyautogui

class Monitors():
    res: tuple

    def __init__(self):
        self.monitors = get_monitors()
        self.number_of_monitors = len(self.monitors)
        self.focused_monitor = self.find_monitor_focus()

    def find_monitor_focus(self) -> int:
        mouse_coordinates = pyautogui.position()
        for i, m in enumerate(self.monitors):
            if m.x < mouse_coordinates[0] < m.x + m.width\
                    and m.y < mouse_coordinates[1] < m.y + m.height:
                self.res = [m.width, m.height, m.x, m.y]
                return i