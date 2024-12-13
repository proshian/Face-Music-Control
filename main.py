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
from visualizer import VizualizaiotnAssembler
from fer_snes_vizualization import FerSensorPartialVizualizationCreator
from camera_vizualization import CameraPartialVizualizationCreator


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

    # Create partial visualizations creators
    camera_viz_ctor = CameraPartialVizualizationCreator(camera, view.image_label)
    fer_sens_viz_ctor = FerSensorPartialVizualizationCreator(fer_sens, camera_viz_ctor)

    camera_sensors_vizualizer = VizualizaiotnAssembler([camera_viz_ctor, fer_sens_viz_ctor], view.image_label)

    controller = Controller(
        viz_list = [camera_sensors_vizualizer], cc_sender = cc_sender, 
        sensors = sensors, resources = resources, ui = view)
    
    view.set_controller(controller)

    view.show()

    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()