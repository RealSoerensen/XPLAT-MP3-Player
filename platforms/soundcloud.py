from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class SoundCloud(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle("Add from SoundCloud")
