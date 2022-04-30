import sys

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel

__version__ = "0.1"
__author__ = "Garri Proshian"



# Create a subclass of QMainWindow to setup the FMC GUI
class FmcUi(QMainWindow):

    def __init__(self):
        super().__init__()
        
        
        
        self._create_play_mode_view()
        self._create_settings_view()

        # ! не до конца понимаю, почему передаем self.
        # В документации вроде написаноЮ что принимается родитель.
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.play_mode_layout)



        self.setWindowTitle("Face Music Control")
        self.resize(*self._initial_size)

    def _create_play_mode_view(self):
        self.play_mode_layout = QHBoxLayout()

        self.image_label = QLabel()
        self.image_label.resize(1, 40)
        self.image_label.setStyleSheet("background-color: lightgreen")

        self.values_layout = QVBoxLayout()

        self.play_mode_layout.addWidget(self.image_label)
        self.play_mode_layout.addLayout(self.values_layout)

    def resizeEvent(self, event):
        """
        ниже закомментирована моя попытка
        запретить непропорциональные изменения размеров
        """
        print("Window has been resized")
        # QMainWindow.resizeEvent(self, event)
        # width = self._centralWidget.width()
        #print(f"{ }")
        # self.resize(width, self.get_new_height(width))
        QMainWindow.resizeEvent(self, event)


    def _create_settings_view(self):
        layout = QHBoxLayout()
    
    
    left_width = 40
    right_width = 40

    _initial_size = (860, 620)

    def get_new_height(self, width):
        return round(self._initial_size[1] * width /  self._initial_size[0])


def main():
    fmc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = FmcUi()
    view.show()
    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()
