import os
import time
import cv2
import pyperclip
from textget.gettext import GetTxt
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog
from PyQt5.Qt import QMainWindow
from PyQt5.QtCore import Qt, QObject, QRect, QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon


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
        self.icon_path = self.local_path + "/resources"
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
        self.menu_buttons()

    def window_setting(self):
        self.setMouseTracking(True)
        self.acceptDrops()
        self.label.setPixmap(self.pixmap)
        self.move(self.geometry[2], self.geometry[3])
        self.showFullScreen()
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.translucent.resize(self.width(), self.height())

    def close_app(self):
        self.close()
        self.SIGNALS.CLOSE.emit()
        self.translucent.SIGNALS.CLOSE.emit()


    # The functions that the buttons will execute
    def click_save_button(self):
        if os.path.exists(self.local_path + "/resources/im.png"):
            file_name = QFileDialog.getSaveFileName(self, "Save File", os.environ['HOMEDRIVE'] + "/Desktop",
                                                    "Images (*.png *.xpm *.jpg)")

            if file_name and file_name[0]:
                self.img_pil.save(file_name[0])

        self.close_app()

    def click_copytext_button(self):
        self.close_app()
        if os.path.exists(self.local_path + "/resources/im.png"):
            textRead = GetTxt(self.local_path + "/resources/im.png")
            textRead.read_text()
            pyperclip.copy(textRead.get_text())

    def click_cancel_button(self):
        self.close_app()

    # Button related functions
    def menu_popdown_animation(self):
        time.sleep(0.01)
        self.button_save.move(30, 30)

    def menu_buttons_geometry(self):
        self.button_save.setGeometry(self.geometry[0] / 2 - 1.2 * self.button_size + 3, 0, self.button_size + 0.2 * self.button_size,
                                     self.button_size)
        self.button_copytext.setGeometry(self.geometry[0] / 2 + 1, 0, self.button_size + 0.2 * self.button_size,
                                         self.button_size)
        self.button_cancel.setGeometry(self.geometry[0] / 2 + 1.2*self.button_size - 2, 0,
                                       self.button_size + 0.2 * self.button_size, self.button_size)

    def menu_buttons_style(self):
        self.button_stylesheet = """
            QPushButton {
                background-color: #2f2f2f; 
                border: none; 
            }
            QPushButton:hover{
                background-color: #707070;
            }
        """
        self.button_save.setStyleSheet(self.button_stylesheet)

        self.button_copytext.setStyleSheet(self.button_stylesheet)
        self.button_cancel.setStyleSheet(self.button_stylesheet)

    def menu_buttons(self):
        self.button_size = 2.9/100 * self.geometry[0]
        self.button_save = QPushButton(self)
        self.button_copytext = QPushButton(self)
        self.button_cancel = QPushButton(self)

        self.menu_buttons_geometry()
        # self.menu_popdown_animation()
        self.menu_buttons_style()

        self.button_save.setIcon(QIcon(self.icon_path + "/save_icon.png"))
        self.button_copytext.setIcon(QIcon(self.icon_path + "/copytext_icon.png"))
        self.button_cancel.setIcon(QIcon(self.icon_path + "/cancel_icon.png"))

        self.button_save.setIconSize(QSize(self.button_size/2.2, self.button_size/2.2))
        self.button_copytext.setIconSize(QSize(self.button_size/3.5, self.button_size/3.5))
        self.button_cancel.setIconSize(QSize(self.button_size/3.5, self.button_size/3.5))

        self.button_save.clicked.connect(self.click_save_button)
        self.button_copytext.clicked.connect(self.click_copytext_button)
        self.button_cancel.clicked.connect(self.click_cancel_button)

        self.button_save.show()
        self.button_copytext.show()
        self.button_cancel.show()


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
        img = cv2.imread(self.image_path)
        img = img[y_first:y_second+1, x_first:x_second+1]
        return revert, img

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        img = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        return img

    def highlight_image(self, cv_img):
        image = self.convert_cv_qt(cv_img)
        image_pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(image_pixmap)
        self.image_label.resize(image_pixmap.width(), image_pixmap.height())

    def setApp(self, app):
        self.app = app

    def mousePressEvent(self, event):
        self.coords.set_first(event.x(), event.y())

    def mouseMoveEvent(self, event):
        self.image_label.setStyleSheet("border: 1px solid white")
        if not self.coords.is_empty():
            revert, img = self.crop_image(self.coords.first.x, self.coords.first.y, event.x(), event.y())
            self.highlight_image(img)
            if revert == 0:
                self.image_label.move(self.coords.first.x, self.coords.first.y)
            elif revert == 1:
                self.image_label.move(event.x(), self.coords.first.y)
            elif revert == 2:
                self.image_label.move(self.coords.first.x, event.y())
            elif revert == 3:
                self.image_label.move(event.x(), event.y())


    def mouseReleaseEvent(self, event):
        revert, img = self.crop_image(self.coords.first.x, self.coords.first.y, event.x(), event.y())
        self.highlight_image(img)
        if revert == 0:
            self.image_label.move(self.coords.first.x, self.coords.first.y)
        elif revert == 1:
            self.image_label.move(event.x(), self.coords.first.y)
        elif revert == 2:
            self.image_label.move(self.coords.first.x, event.y())
        elif revert == 3:
            self.image_label.move(event.x(), event.y())

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img_pil = Image.fromarray(img)
        self.img_pil.save("resources/im.png")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_app()
