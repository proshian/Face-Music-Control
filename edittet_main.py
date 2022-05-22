import sys

from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt

from sensor import Sensor
from fmc_ui import FmcUi
from rand_sens import rand_sens
# from fer_sens import fer_sens
from cc_sender import CcSender



def main():
    fmc = QApplication(sys.argv)
    fmc.setStyle('Fusion')

    """
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.white)
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    fmc.setPalette(palette)
    """

    # ! Следует реализовать окно, возникающее, если нет доступных MIDI портов.
    # Это приложение, проверяющее раз в 50 миллисекунд, что порт появился.
    # Как только порт появляется, данное окно закрывается и открывается FMC.
    cc_sender = CcSender(Sensor.all_sensors)
    view = FmcUi(Sensor.all_sensors, cc_sender)
    view.show()
    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()