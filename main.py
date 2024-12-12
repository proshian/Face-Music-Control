import sys
from typing import List

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

from sensor import Sensor
from fmc_ui import FmcUi
from fer_sens import (
    FerSensor, emotions_icons, emotions, model_dir, model_weights_dir)
from cc_sender import CcSender
from controller import Controller
from fmc_resource import Resource
from camera import Camera
from visualizer import Vizualizer


def set_up_app() -> QApplication:
    fmc = QApplication(sys.argv)
    
    QtGui.QFontDatabase.addApplicationFont('./Roboto/Roboto-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('./Roboto/Roboto-Bold.ttf')

    fmc.setStyle('Fusion')

    file = open("style.qss",'r')

    with file:
        qss = file.read()
        fmc.setStyleSheet(qss)

    # palette = QPalette()
    # palette.setColor(QPalette.Window, Qt.white)
    # palette.setColor(QPalette.Button, QColor(255, 255, 255))
    # fmc.setPalette(palette)

    return fmc

def main() -> None:
    camera = Camera()
    resources: List[Resource] = [camera]
    
    fer_sens = FerSensor(emotions, emotions_icons, camera, 0, 1, model_dir, model_weights_dir)
    sensors: List[Sensor] = [fer_sens]

    cc_sender = CcSender(sensors)
    
    fmc = set_up_app()
    
    # создание окна
    view = FmcUi(sensors, cc_sender)

    # Внесение элемента граф. интерфейса в качестве поля камеры. 
    # Необходимо для масштабирования её визуализации
    # и визуализаций, накладывающихся на нее
    camera.set_label(view.image_label)

    camera_vizualizer = Vizualizer([camera, fer_sens], view.image_label)

    controller = Controller(
        viz_list = [camera_vizualizer], cc_sender = cc_sender, 
        sensors = sensors, resources = resources, ui = view)
    
    view.set_controller(controller)

    view.show()

    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()