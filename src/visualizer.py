from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
from PIL import Image
import numpy as np

# The imports below are for type hints
from typing import List
from PyQt5.QtWidgets import QLabel
from partial_visualizations.partial_vizualization_creator import PartialVisualizationCreator


class VisualizaiotnAssembler():
    """
    VisualizaiotnAssembler принимает:
    1. Cписок source_list источников, обладающих визуализацией.
       Это объекты PartialVisualizationCreator, у которых можно получить
       RGBA изображение в виде np.ndarray. 
       Визуализатор накладывает визуализации друг на друга и отображает
       конечное изображение в элементе графического интерфейса img_qlabel.
       source_list[0].vizualisation хранит самый нижний слой,
       source_list[-1].vizualisation — самый верхний слой
    
    2. QLabel img_qlabel, в котором VisualizaiotnAssembler отрисовывает изображение,
       полученное альфа-композицией визуализаций источников.  
    """
    def __init__(self, 
                 source_list: List[PartialVisualizationCreator],
                 img_qlabel: QLabel) -> None:
        self._img_qlabel = img_qlabel
        self._source_list = source_list

    def _np_RGB_to_QPixmap(np_RGB: np.ndarray) -> QPixmap:
        """
        Приведение RGB изображения,
        предстваленного в виде np.ndarray к QPixmap
        """
        height, width, _ = np_RGB.shape
        bytesPerLine = 3 * width
        qImg = QImage(np_RGB.data, width, height, bytesPerLine, QImage.Format_RGB888)
        qpixmap = QPixmap(qImg)
        return qpixmap
    
    def alpha_compose(background: np.ndarray, foreground: np.ndarray):
        compose = Image.alpha_composite(
            Image.fromarray(background),
            Image.fromarray(foreground))
        return np.array(compose)

    def _gather_visualization(self):
        visualization = self._source_list[0].get_vizualization()
        for source in self._source_list[1:]:
            visualization = VisualizaiotnAssembler.alpha_compose(
                visualization, source.get_vizualization())
        return visualization
    
    def visualize(self):
        visualization = self._gather_visualization()
        visualization = cv2.cvtColor(visualization, cv2.COLOR_RGBA2RGB)
        qpixmap = VisualizaiotnAssembler._np_RGB_to_QPixmap(visualization)
        qpixmap = qpixmap.scaled(
            self._img_qlabel.width(),
            self._img_qlabel.height(),
            Qt.KeepAspectRatioByExpanding)

        self._img_qlabel.setPixmap(qpixmap)

    # def update_scaling_factor(self):
    #     self._source_list[0].update_scaling_factor()

