import sys

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QIcon

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

        self._create_values_layout(["happy", "sad"])

        self.play_mode_layout.addWidget(
            self.image_label, self.left_right_proportion[0])
        self.play_mode_layout.addLayout(
            self.values_layout, self.left_right_proportion[1])

    def _create_values_layout(self, names):
        self.values_layout = QVBoxLayout()
        for name in names:
            label = QLabel(name)
            label.setStyleSheet("background-color: blue")
            self.values_layout.addWidget(label, 1)
        settings_button_container = QWidget()
        settings_button = QPushButton()
        settings_button.setGeometry(200, 150, 100, 40)
        settings_button.setIcon(QIcon('emojis/settings.svg'))
        self.values_layout.addWidget(settings_button_container, 4)
        self.values_layout.addWidget(settings_button)
        
                

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
    
    
    #left_width = 40
    #right_width = 40
    left_right_proportion = (5,1)

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
