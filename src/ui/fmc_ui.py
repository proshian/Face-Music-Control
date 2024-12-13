from functools import partial

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QStackedWidget,
)
from PyQt5.QtGui import QIcon, QFont
import numpy as np

from .shadow_button import ShadowButton


__version__ = "0.1"
__author__ = "Garri Proshian"

class SwitchButton(QPushButton):
    def __init__(self):
        super().__init__(flat = True)



class FmcUi(QMainWindow):
    """
    Класс главного окна Face Music Control.
    """
    def __init__(self, sensors, cc_sender, controller = None):
        super().__init__()
        
        
        self._sensors = sensors
        # self.labels: dict(int sensor_id: list(Qlabel) ) 
        self.labels = dict()
        self.active_label_index = None
        # self.binding_buttons = dict()

        self._set_fonts()
        
        self._create_mode_buttons() 

        self._create_play_mode_widget()
        self._create_settings_widget(cc_sender)

        self._centralWidget = QStackedWidget(self)
        self.setCentralWidget(self._centralWidget)

        right_bar_color = "#E9E9ED"
        self._centralWidget.setStyleSheet(f"background-color: {right_bar_color}")
        
        self._centralWidget.addWidget(self.play_mode_widget)
        self._centralWidget.addWidget(self.settings_widget)

        self.setWindowTitle("Face Music Control")
        self.resize(*self._initial_size)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        self.timer = QTimer()
        
        self.turn_on_play_mode()


    def _create_mode_buttons(self):
        self.mode_buttons_bar_color = "#293A4C"
        self.active_mode_button_back_color = "#17212B"
        self.active_setting_mode_icon = QIcon('assets/icons/active_settings.svg')
        self.disabled_setting_mode_icon = QIcon('assets/icons/disabled_settings.svg')
        self.disabled_play_mode_icon = QIcon('assets/icons/disabled_playmode.svg')
        self.active_play_mode_icon = QIcon('assets/icons/active_playmode.svg')

        self.play_button = SwitchButton()
        self.play_button.setIconSize(QSize(50, 60))
        self.play_button.setFixedSize(QSize(90, 60))
        self.play_button.clicked.connect(self.turn_on_play_mode)
        # self.play_button.setContentsMargins(0,0,0,0)

        self.settings_button = SwitchButton()
        self.settings_button.setIconSize(QSize(50, 60))
        self.settings_button.setFixedSize(QSize(90, 60))
        self.settings_button.clicked.connect(self.turn_on_settings_mode)
        # self.settings_button.setContentsMargins(0,0,0,0)

        self.mode_buttons_layout = QHBoxLayout()
        self.mode_buttons_layout.setSpacing(0)
        self.mode_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.mode_buttons_layout.addWidget(self.play_button)
        self.mode_buttons_layout.addWidget(self.settings_button)

        self.mode_buttons_widget = QWidget()
        

        self.mode_buttons_widget.setLayout(self.mode_buttons_layout)
    



    def set_controller(self, controller):
        """
        Предполагается, что будет вызвана единожды.
        Если пользователь будет использовать этот метод, неоднократно
        стоит проверять, есть ли связанные с событием timeout функции
        и дисконнектить их так: self.timer.timeout.disconnect(self.playmode_loop)
        """
        self.playmode_loop = controller.loop
        self.timer.timeout.connect(self.playmode_loop)

    def _create_play_mode_widget(self):
        self.play_mode_widget = QWidget()
        

        play_mode_layout = QHBoxLayout()
        play_mode_layout.setSpacing(0)
        play_mode_layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.image_label.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        # self.image_label.setStyleSheet("background-color: lightgreen")

        self._create_values_layout()

        vals_widget = QWidget()
        vals_widget.setLayout(self.play_mode_right)
        vals_widget.setFixedWidth(self._right_width)

        play_mode_layout.addWidget(self.image_label)
        play_mode_layout.addWidget(vals_widget)
        
        self.play_mode_widget.setLayout(play_mode_layout)


    def _create_values_layout(self):
        self.play_mode_right = QVBoxLayout()
        self.play_mode_right.setContentsMargins(0,0,0,0)

        self.values_layout = QVBoxLayout()
        self.values_layout.setContentsMargins(0,28,0,28)
        self.values_layout.setSpacing(14)

        for sensor in self._sensors: 
            sensor_labels = []
            # Возможно, буду использовать здесь иконки
            # for name, _ in zip(sensor.names, sensor.icon_locations):
            for name in sensor.names:
                label = QLabel(f"{name}:")
                label.setFont(self.regular_label_font)
                #label.setStyleSheet("background-color: blue")
                label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 

                value = QLabel("none")
                value.setFont(self.regular_label_font)
                #value.setStyleSheet("background-color: red")
                value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter) 
                

                line = QHBoxLayout()
                line.setContentsMargins(0,0,0,0)
                line.addWidget(label, 3)
                line.addWidget(value, 2)

                line_widget = QWidget()
                line_widget.setFixedHeight(60)
                #line_widget.setStyleSheet("background-color: black")
                line_widget.setLayout(line)

                self.values_layout.addWidget(line_widget)

                sensor_labels.append({'label':label, 'value':value})
            self.labels[sensor.id] = sensor_labels
        
        self.play_mode_right.addLayout(self.values_layout)

        
        # settings_button.setGeometry(200, 150, 100, 40)
       

    def _update_labels(self, sensor_id, results):
        if self.active_label_index is not None:
            self.labels[sensor_id][self.active_label_index]['value'].setFont(
                self.regular_label_font)
            self.labels[sensor_id][self.active_label_index]['label'].setFont(
                self.regular_label_font)
        
        self.active_label_index = np.argmax(results)

        self.labels[sensor_id][self.active_label_index]['value'].setFont(
            self.max_label_font)
        self.labels[sensor_id][self.active_label_index]['label'].setFont(
            self.max_label_font)

        for i, result in enumerate(results):
            self.labels[sensor_id][i]['value'].setText(f"{result:.2f}")

    def _create_settings_widget(self, cc_sender):
        self.settings_widget = QWidget()
        self.settings_widget.setContentsMargins(0,0,0,0)

        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(0)
        settings_layout.setContentsMargins(0,0,0,0)

        temp_placeholder = QLabel()
        # temp_placeholder.resize(1, 40)
        temp_placeholder.setStyleSheet("background-color: white")
        temp_placeholder.setContentsMargins(0,0,0,0)

        self._create_buttons_layout(cc_sender)

        settings_right_widget = QWidget()
        settings_right_widget.setLayout(self.buttons_layout)
        settings_right_widget.setFixedWidth(self._right_width)

        settings_layout.addWidget(temp_placeholder)
        settings_layout.addWidget(settings_right_widget)
        
        self.settings_widget.setLayout(settings_layout)




    def _create_buttons_layout(self, cc_sender):
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        emoji_buttons_layout = QVBoxLayout()
        emoji_buttons_layout.setContentsMargins(0, 28, 0, 28)
        emoji_buttons_layout.setSpacing(14)
        
        for sensor in self._sensors:
            # Возможно, буду использовать здесь названия 
            # for _, icon in zip(sensor.names, sensor.icon_locations):
            for index, icon in enumerate(sensor.icon_locations):
                button = ShadowButton()
                button.setIcon(QIcon(icon))
                button.clicked.connect(
                    partial(cc_sender.learn, sensor_id = sensor.id, index = index))
                emoji_buttons_layout.addWidget(button, 1, alignment= Qt.AlignHCenter)

        self.buttons_layout.addLayout(emoji_buttons_layout)


    def turn_on_settings_mode(self):
        self._centralWidget.setCurrentWidget(self.settings_widget)
        self.timer.stop()
        self.buttons_layout.addWidget(self.mode_buttons_widget, alignment= Qt.AlignBottom)
        self.play_button.setStyleSheet(
            f"background-color: {self.mode_buttons_bar_color}")
        self.settings_button.setStyleSheet(
            f"background-color: {self.active_mode_button_back_color}")
        self.play_button.setIcon(self.disabled_play_mode_icon)
        self.settings_button.setIcon(self.active_setting_mode_icon)
        # self.always_top()
    
    def turn_on_play_mode(self):
        self._centralWidget.setCurrentWidget(self.play_mode_widget)
        self.timer.start(self.playmode_loop_len)
        self.play_mode_right.addWidget(self.mode_buttons_widget, alignment= Qt.AlignBottom)
        self.settings_button.setStyleSheet(
            f"background-color: {self.mode_buttons_bar_color}")
        self.play_button.setStyleSheet(
            f"background-color: {self.active_mode_button_back_color}")
        self.play_button.setIcon(self.active_play_mode_icon)
        self.settings_button.setIcon(self.disabled_setting_mode_icon)
        # self.not_always_top()
    
    def _set_fonts(self):
        self.regular_label_font = QFont("Roboto")
        self.regular_label_font.setPointSizeF(9.5)

        self.max_label_font = QFont("Roboto")
        self.max_label_font.setPointSizeF(9.5)
        self.max_label_font.setBold(True)

        
    # Хотелось бы, чтобы в режиме настройки окно приложения было выше всех,
    # а в режиме игры вело себя как обычное окно.
    # Смена флагов приводит к приостанвке рендеринга.
    # Получемое мелькание раздрожает. Поэтому временно отказываюсь от идеи.
    # def always_top(self):
    #     self.setWindowFlags(Qt.WindowStaysOnTopHint)
    #     self.show()
    # 
    # def not_always_top(self):
    #     self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)
    #     self.show()
    
    _right_width = 180

    # Раз в 41 милисекунду соответствовало бы 24 срабатываниям в секунду.
    # Разница между 41 и 55 не ощутима (изображение отстает одиакого),
    # однако это в 1.4 раза меьше вычислений.
    playmode_loop_len = 50

    _initial_size = (820, 628)

    def get_new_height(self, width):
        return round(self._initial_size[1] * width /  self._initial_size[0])
