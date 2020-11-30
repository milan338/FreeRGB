from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal


# QPushButton that detects when hovered
class HoverButton(QPushButton):
    mouse_hovered = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.mouse_hovered.emit(True)

    def leaveEvent(self, event):
        self.mouse_hovered.emit(False)
