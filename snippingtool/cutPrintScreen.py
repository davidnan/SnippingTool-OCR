import os
import time
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.Qt import QMainWindow
from PyQt5.QtCore import Qt, QObject, QRect
from PyQt5.QtGui import QPixmap, QImage


class Pair():
    x: int
    y: int

    def clear(self):
        self.x = 0
        self.y = 0

class Coordinates():


    def __init__(self):
        self.first = Pair()
        self.second = Pair()
        self.empty = True

    def set_first(self, x, y):
        self.empty = False
        self.first.x = x
        self.first.y = y

    def set_second(self, x, y):
        self.empty = False
        self.second.x = x
        self.second.y = y

    def get_first(self):
        return (self.first.x + self.first.y)

    def get_second(self):
        return(self.second.x, self.second.y)

    def get(self):
        return (self.get_first(), self.get_second())

    def clear(self):
        self.empty = True
        self.first.clear()
        self.second.clear()

    def is_empty(self):
        return self.empty

class CutPsSignals(QObject):
   CLOSE = QtCore.pyqtSignal()

class TranslucentOverlay(QWidget):
    def __init__(self, parent, color):
        super(TranslucentOverlay, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.fillColor = QtGui.QColor(*color)
        self.penColor = QtGui.QColor("#333333")

        self.SIGNALS = CutPsSignals()

    # def animation(self):

    def paintEvent(self, event):
        s = self.size()
        self.qp = QtGui.QPainter()
        self.rect = QRect(0, 0, s.width(), s.height())
        self.qp.begin(self)
        self.qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.qp.setPen(self.penColor)
        self.qp.setBrush(self.fillColor)
        self.qp.drawRect(self.rect)

        self.qp.end()

    def _onclose(self):
        self.SIGNALS.CLOSE.emit()

class CutPS(QMainWindow):
    app: QApplication
    coords: Coordinates()

    def __init__(self, image_path, focused_monitor, monitor_res):
        super().__init__()
        self.image_path = image_path
        self.local_path = os.path.abspath(os.getcwd())
        self.focused_monitor = focused_monitor
        self.geometry = monitor_res
        self.coords = Coordinates()
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.image_path)
        self.SIGNALS = CutPsSignals()

        self.black_translucent = (0, 0, 0, 120)
        self.translucent = TranslucentOverlay(self, self.black_translucent)

        self.image_label = QLabel(self)

        self.window_setting()

    def window_setting(self):
        self.setMouseTracking(True)
        self.acceptDrops()
        self.label.setPixmap(self.pixmap)
        self.move(self.geometry[2], self.geometry[3])
        self.showFullScreen()
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.translucent.resize(self.width(), self.height())


    def clean_coords(self, x_first, y_first, x_second, y_second):
        revert = 0
        if x_first > x_second:
            revert += 1
            aux = x_second
            x_second = x_first
            x_first = aux
        if y_first > y_second:
            revert += 2
            aux = y_second
            y_second = y_first
            y_first = aux

        return x_first, y_first, x_second, y_second, revert

    def crop_image(self, x_first, y_first, x_second, y_second):
        x_first, y_first, x_second, y_second, revert = self.clean_coords(x_first, y_first, x_second, y_second)
        img = Image.open(self.image_path)
        img = img.crop((x_first, y_first, x_second + 1, y_second + 1))
        img.save("im.png")
        return revert

    def highlight_image(self):
        image_pixmap = QPixmap(self.local_path + "\im.png")
        self.image_label.setPixmap(image_pixmap)
        self.image_label.resize(image_pixmap.width(), image_pixmap.height())

    def setApp(self, app):
        self.app = app

    def mousePressEvent(self, event):
        self.coords.set_first(event.x(), event.y())

    def mouseMoveEvent(self, event):
        self.image_label.setStyleSheet("border: 2px solid white")
        if not self.coords.is_empty():
            revert = self.crop_image(self.coords.first.x, self.coords.first.y, event.x(), event.y())
            self.highlight_image()
            if revert == 0:
                self.image_label.move(self.coords.first.x, self.coords.first.y)
            elif revert == 1:
                self.image_label.move(event.x(), self.coords.first.y)
            elif revert == 2:
                self.image_label.move(self.coords.first.x, event.y())
            elif revert == 3:
                self.image_label.move(event.x(), event.y())


    def mouseReleaseEvent(self, event):
        revert = self.crop_image(self.coords.first.x, self.coords.first.y, event.x(), event.y())
        self.highlight_image()
        if revert == 0:
            self.image_label.move(self.coords.first.x, self.coords.first.y)
        elif revert == 1:
            self.image_label.move(event.x(), self.coords.first.y)
        elif revert == 2:
            self.image_label.move(self.coords.first.x, event.y())
        elif revert == 3:
            self.image_label.move(event.x(), event.y())


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.highlight_image()

        if event.key() == Qt.Key_Escape:
            self.close()
            self.SIGNALS.CLOSE.emit()
            self.translucent.SIGNALS.CLOSE.emit()
