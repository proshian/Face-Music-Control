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

def main():
    fmc = QApplication(sys.argv)
    fmc.setStyle('Fusion')
    
    cc_sender = CcSender(Sensor.all_sensors)

    camera = Camera()

    fer_sens = FerSensor(emotions, emotions_icons, camera, 0, 1, KMU_dir)

    controller = Controller(
        camera, cc_sender, Sensor.all_sensors, Resource.all_resources)

    view = FmcUi(Sensor.all_sensors, cc_sender, controller)
    view.show()
    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()