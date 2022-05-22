import sys

from PyQt5.QtWidgets import QApplication

from sensor import Sensor
from fmc_ui import FmcUi
from rand_sens import rand_sens
from fer_sens import fer_sens
from cc_sender import CcSender



def main():
    fmc = QApplication(sys.argv)
    fmc.setStyle('Fusion')
    
    cc_sender = CcSender(Sensor.all_sensors)
    view = FmcUi(Sensor.all_sensors, cc_sender)
    view.show()
    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()