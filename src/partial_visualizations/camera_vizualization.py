from typing import List

import cv2
from PyQt5.QtWidgets import QLabel

from resources.camera import Camera
from .partial_vizualization_creator import PartialVizualizationCreator

class CameraPartialVizualizationCreator(PartialVizualizationCreator):
    def __init__(self, camera: Camera, img_label: QLabel) -> None:
        self.camera = camera
        self.img_label = img_label
        self._scaling_factor = 1.0
        self.viz_shape = self.camera.cur_data.shape[:2][::-1]


    def get_vizualization(self):
        return self.visualization

    @property
    def visualization(self):
        self.update_scaling_factor()
        viz = cv2.resize(self.camera.cur_data, self.get_viz_shape())
        return cv2.cvtColor(viz, cv2.COLOR_RGB2RGBA)

    def get_cur_data_wh_ratio(self) -> float:
        """Отношение ширины к высоте в исходном изображении с камеры"""
        return self.camera.cur_data.shape[1] / self.camera.cur_data.shape[0]

    def update_scaling_factor(self) -> None:
        label_width = self.img_label.width()
        label_height = self.img_label.height()
        label_wh_ratio = label_width / label_height
        cur_data_wh_ratio = self.get_cur_data_wh_ratio()

        if label_wh_ratio > cur_data_wh_ratio:
            scaling_factor = label_width / self.camera.cur_data.shape[1]
        else:
            scaling_factor = label_height / self.camera.cur_data.shape[0]

        self._scaling_factor = scaling_factor
        self.update_viz_shape()


    def update_viz_shape(self) -> None:
        self.viz_shape = list(
            map(lambda x: round(x*self._scaling_factor),
                self.camera.cur_data.shape[:2][::-1]))

    def get_viz_shape(self) -> List[int]:
        """Возвращает список [ширина, высота]"""
        return self.viz_shape
