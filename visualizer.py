from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
from PIL import Image
import numpy as np

class Vizualizer():
    def __init__(self, source_list, img_qlabel):
        self._img_qlabel = img_qlabel
        self._source_list = source_list

    def _np_RGB_to_QPixmap(np_RGB):
        height, width, _ = np_RGB.shape
        bytesPerLine = 3 * width
        qImg = QImage(np_RGB.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qpixmap = QPixmap(qImg)
        return qpixmap
    
    def alpha_compose(background, foreground):
        compose = Image.alpha_composite(
            Image.fromarray(background),
            Image.fromarray(foreground))
        return np.array(compose)

    def _gather_visualization(self):
        visualization = self._source_list[0].visualization
        for source in self._source_list[1:]:
            # ! PEP8
            visualization = Vizualizer.alpha_compose(visualization, source.visualization)
        return visualization
    
    def visualize(self):
        visualization = self._gather_visualization()
        visualization = cv2.cvtColor(visualization, cv2.COLOR_RGBA2RGB)
        qpixmap = Vizualizer._np_RGB_to_QPixmap(visualization)
        qpixmap = qpixmap.scaled(
            self._img_qlabel.width(),
            self._img_qlabel.height(),
            Qt.KeepAspectRatioByExpanding)
            # Qt.KeepAspectRatioByExpanding)

        self._img_qlabel.setPixmap(qpixmap)

    def update_scaling_factor(self):
        self._source_list[0].update_scaling_factor()

            

    """
    def _set_img_qlabel(self, img_qlabel):
        self._img_qlabel = img_qlabel
    """