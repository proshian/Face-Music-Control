from PyQt5.QtWidgets import (
    QPushButton,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QRgba64

class ShadowButton(QPushButton):
    def __init__(self) -> None:
        super().__init__(flat = True)
        self.create_and_set_shadow()
        self.enterEvent = self.create_and_set_big_shadow
        self.leaveEvent = self.create_and_set_shadow
        self.pressed.connect(self.create_and_set_active_shadow)
        self.released.connect(self.create_and_set_big_shadow)
        

    def create_and_set_shadow(self, event = None):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(13)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(QRgba64.fromRgba(19, 23, 27, 26)))
        self.setGraphicsEffect(shadow)

    def create_and_set_big_shadow(self, event = None):
        big_shadow = QGraphicsDropShadowEffect()
        big_shadow.setBlurRadius(16)
        big_shadow.setXOffset(0)
        big_shadow.setYOffset(0)
        big_shadow.setColor(QColor(QRgba64.fromRgba(19, 23, 27, 77)))
        self.setGraphicsEffect(big_shadow)

    def create_and_set_active_shadow(self, event = None):
        big_shadow = QGraphicsDropShadowEffect()
        big_shadow.setBlurRadius(16)
        big_shadow.setXOffset(0)
        big_shadow.setYOffset(0)
        big_shadow.setColor(QColor(QRgba64.fromRgba(0, 128, 244, 240)))
        self.setGraphicsEffect(big_shadow)
        