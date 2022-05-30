from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2

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
        alpha_background = background[:,:,3] / 255.0
        alpha_foreground = foreground[:,:,3] / 255.0

        # set adjusted colors
        for color in range(0, 3):
            background[:,:,color] = alpha_foreground * foreground[:,:,color] + \
                alpha_background * background[:,:,color] * (1 - alpha_foreground)

        # set adjusted alpha and denormalize back to 0-255
        background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255

    def _gather_visualization(self):
        visualization = self._source_list[0].visualization
        for source in self._source_list[1:]:
            Vizualizer.alpha_compose(visualization, source.visualization)
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

            

    """
    def _set_img_qlabel(self, img_qlabel):
        self._img_qlabel = img_qlabel
    """