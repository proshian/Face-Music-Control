import sys

from PyQt5.QtWidgets import QApplication

from sensor import Sensor
from fmc_ui import FmcUi
#from rand_sens import rand_sens
from fer_sens import FerSensor, KMU_dir, emotions_icons, emotions
from cc_sender import CcSender
from controller import Controller
from resource import Resource
from camera import Camera
from visualizer import Vizualizer

def main():
    camera = Camera()

    fer_sens = FerSensor(emotions, emotions_icons, camera, 0, 1, KMU_dir)


    # ! Следует реализовать окно, возникающее, если нет доступных MIDI портов.
    # Это приложение, проверяющее раз в 50 миллисекунд, что порт появился.
    # Как только порт появляется, данное окно закрывается и открывается FMC.
    cc_sender = CcSender(Sensor.all_sensors)
    
    

    fmc = QApplication(sys.argv)
    fmc.setStyle('Fusion')

    
    """
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.white)
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    fmc.setPalette(palette)
    """

    view = FmcUi(Sensor.all_sensors, cc_sender)

    camera_vizualizer = Vizualizer([camera], view.image_label)

    controller = Controller(
        [camera_vizualizer], cc_sender,
        Sensor.all_sensors, Resource.all_resources)
    
    #view.set_controller(controller)

    view.show()
    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()