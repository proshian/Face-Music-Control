import sys
from typing import NoReturn

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

from sensor import Sensor
from fmc_ui import FmcUi
#from rand_sens import rand_sens
from fer_sens import FerSensor, KMU_dir, emotions_icons, emotions
from cc_sender import CcSender
from controller import Controller
from resource import Resource
from camera import Camera
from visualizer import Vizualizer

def set_up_app() -> QApplication:
    fmc = QApplication(sys.argv)
    
    QtGui.QFontDatabase.addApplicationFont('./Roboto/Roboto-Regular.ttf')
    # QtGui.QFontDatabase.addApplicationFont('./Roboto/Roboto-Medium.ttf')
    QtGui.QFontDatabase.addApplicationFont('./Roboto/Roboto-Bold.ttf')

    fmc.setStyle('Fusion')

    file = open("style.qss",'r')

    with file:
        qss = file.read()
        fmc.setStyleSheet(qss)
    """
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.white)
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    fmc.setPalette(palette)
    """
    return fmc

def main() -> NoReturn:
    # Создадим все требующиеся объекты наследников Resource (только camera)
    camera = Camera()

    # Создадим все требующиеся объекты наследников Sensor (только fer_sens)
    fer_sens = FerSensor(emotions, emotions_icons, camera, 0, 1, KMU_dir)

    # ! Можно добавить окно, возникающее, если нет доступных MIDI портов.
    # и проверяющее раз в n миллисекунд, наличие порта.
    # Когда порт появляется, данное окно закрывается и открывается FmcUi.
    cc_sender = CcSender(Sensor.all_sensors)
    
    
    fmc = set_up_app()
    
    # создание окна
    view = FmcUi(Sensor.all_sensors, cc_sender)

    # Внесение элемента граф. интерфейса в качестве поля камеры. 
    # Необходимо для масштабирования её визуализации
    # и визуализаций, накладывающихся на нее
    camera.set_label(view.image_label)

    camera_vizualizer = Vizualizer([camera, fer_sens], view.image_label)

    controller = Controller(
        [camera_vizualizer], cc_sender, Sensor.all_sensors,
        Resource.all_resources, view)
    
    view.set_controller(controller)

    view.show()

    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()