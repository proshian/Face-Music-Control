import sys
import os

from PyQt5.QtWidgets import QApplication

from fmc_ui import FmcUi
from value_getter import ValueGetter

def main():
    icons_dir = 'emojis/'
    emotions = ["happy", "sad", "angry", "neutral", "surprised"]
    emotions_icons = [os.path.join(icons_dir, f"{emotion}.svg") for emotion in emotions]
    print(emotions_icons)
    FER_nn_dict = {
        "names": emotions,
        "icons": emotions_icons}
    """
    FER_nn = ValueGetter( 
        emotions, icon_locations, getter,
        min_possible, max_possible, bias)
    """

    fmc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = FmcUi([FER_nn_dict])
    view.show()
    sys.exit(fmc.exec_())


if __name__ == "__main__":
    main()