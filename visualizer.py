from PyQt5.QtGui import QImage, QPixmap

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
    
    # ! Реализовать эту функцию
    def _overlay(lower_, upper_):
        return lower_

    def _gather_visualization(self):
        visualization = self._source_list[0].visualization
        for source in self._source_list[1:]:
            visualization = Vizualizer._overlay(
                visualization, source.visualization)
        return visualization
    
    def visualize(self):
        visualization = self._gather_visualization()
        qpixmap = Vizualizer._np_RGB_to_QPixmap(visualization)
        self._img_qlabel.setPixmap(qpixmap)

            

    """
    def _set_img_qlabel(self, img_qlabel):
        self._img_qlabel = img_qlabel
    """