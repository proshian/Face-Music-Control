import os
import sys
from typing import List

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

from sensors.sensor import Sensor
from ui.fmc_ui import FmcUi
from sensors.fer_sens import (
    FerSensor, emotions_icons, emotions, model_dir, model_weights_dir)
from cc_sender import CcSender
from controller import Controller
from resources.fmc_resource import Resource
from resources.camera import Camera
from visualizer import VisualizaiotnAssembler
from partial_visualizations.fer_snes_vizualization import FerSensorPartialVisualizationCreator
from partial_visualizations.camera_vizualization import CameraPartialVisualizationCreator


def set_up_app() -> QApplication:
    fmc = QApplication(sys.argv)
    
    QtGui.QFontDatabase.addApplicationFont('./Roboto/Roboto-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('./Roboto/Roboto-Bold.ttf')

    fmc.setStyle('Fusion')

    with open("./src/ui/style.qss",'r') as f:
        qss = f.read()
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
    camera_viz_ctor = CameraPartialVisualizationCreator(camera, view.image_label)
    fer_sens_viz_ctor = FerSensorPartialVisualizationCreator(fer_sens, camera_viz_ctor)

    camera_sensors_vizualizer = VisualizaiotnAssembler([camera_viz_ctor, fer_sens_viz_ctor], view.image_label)

    controller = Controller(
        viz_list = [camera_sensors_vizualizer], cc_sender = cc_sender, 
        sensors = sensors, resources = resources, ui = view)
    
    view.set_controller(controller)

    view.show()

    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()