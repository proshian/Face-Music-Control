from functools import partial

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtGui import QIcon

__version__ = "0.1"
__author__ = "Garri Proshian"



# Create a subclass of QMainWindow to setup the FMC GUI
class FmcUi(QMainWindow):

    def __init__(self, names_and_labels):
        super().__init__()
        
        
        self.names_and_labels = names_and_labels
        
        self._create_play_mode_widget()
        self._create_settings_widget()

        # ! не до конца понимаю, почему передаем self.
        # В документации вроде написаноЮ что принимается родитель.
        self._centralWidget = QStackedWidget(self)
        self.setCentralWidget(self._centralWidget)
        
        self._centralWidget.addWidget(self.play_mode_widget)
        self._centralWidget.addWidget(self.settings_widget)


        self.setWindowTitle("Face Music Control")
        self.resize(*self._initial_size)


    def _create_play_mode_widget(self):
        self.play_mode_widget = QWidget()

        play_mode_layout = QHBoxLayout()

        self.image_label = QLabel()
        self.image_label.resize(1, 40)
        self.image_label.setStyleSheet("background-color: lightgreen")

        self._create_values_layout()

        play_mode_layout.addWidget(
            self.image_label, self.left_right_ratio[0])
        play_mode_layout.addLayout(
            self.values_layout, self.left_right_ratio[1])
        
        self.play_mode_widget.setLayout(play_mode_layout)


    def _create_values_layout(self):
        self.values_layout = QVBoxLayout()

        for d in self.names_and_labels:
            # Возможно, буду использовать здесь иконки 
            for name, _ in zip(d['names'], d['icons']):
                
                label = QLabel(f"{name}:")
                label.setStyleSheet("background-color: blue")
                label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 

                value = QLabel("none")
                value.setStyleSheet("background-color: red")
                value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter) 
                

                line = QHBoxLayout()
                line.addWidget(label, 3)
                line.addWidget(value, 2)

                self.values_layout.addLayout(line, 1)

        # settings_button_container = QWidget()
        settings_button = QPushButton()

        # settings_button.setGeometry(200, 150, 100, 40)
        #settings_button.setFixedSize(QSize(60, 60))
        settings_button.setIcon(QIcon('emojis/settings.svg'))
        settings_button.setIconSize(QSize(50,50))
        settings_button.clicked.connect(self.turn_on_settings_mode)
        # self.values_layout.addWidget(settings_button_container, 4)
        
        placeholder = QWidget()

        line = QHBoxLayout()
        # line.addWidget(placeholder)
        line.addWidget(settings_button)

        self.values_layout.addLayout(line)

        

    def _create_settings_widget(self):
        self.settings_widget = QWidget()

        settings_layout = QHBoxLayout()

        temp_placeholder = QLabel()
        temp_placeholder.resize(1, 40)
        temp_placeholder.setStyleSheet("background-color: cyan")

        self._create_buttons_layout()

        settings_layout.addWidget(
            temp_placeholder, self.left_right_ratio[0])
        settings_layout.addLayout(
            self.buttons_layout, self.left_right_ratio[1])
        
        self.settings_widget.setLayout(settings_layout)




    def _create_buttons_layout(self):
        self.buttons_layout = QVBoxLayout()

        for d in self.names_and_labels:
            # Возможно, буду использовать здесь названия 
            for _, icon in zip(d['names'], d['icons']):
                
                button = QPushButton()
                button.setIcon(QIcon(icon))
                button.setIconSize(QSize(50,50))
                # settings_button.clicked.connect()

                self.buttons_layout.addWidget(button, 1)

        play_button = QPushButton()

        play_button.setIcon(QIcon('emojis/play.svg'))
        play_button.setIconSize(QSize(50,50))
        play_button.clicked.connect(self.turn_on_play_mode)        

        self.buttons_layout.addWidget(play_button)


    def resizeEvent(self, event):
        pass
        # ниже закомментирована моя попытка
        # запретить непропорциональные изменения размеров

        print("Window has been resized")
        #w = event.size().width()
        #h = event.size().height()

        # print(f"{event.width() = }")
        # QMainWindow.resizeEvent(self, event)
        # width = self._centralWidget.width()
        #print(f"{ }")
        #self.resize(w, self.get_new_height(w))
        # QMainWindow.resizeEvent(self, event)

    def turn_on_settings_mode(self):
        self._centralWidget.setCurrentWidget(self.settings_widget)
    
    def turn_on_play_mode(self):
        self._centralWidget.setCurrentWidget(self.play_mode_widget)
    
    #left_width = 40
    #right_width = 40
    left_right_ratio = (5,1)

    _initial_size = (860, 620)

    def get_new_height(self, width):
        return round(self._initial_size[1] * width /  self._initial_size[0])
