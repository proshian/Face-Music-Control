# from tracemalloc import Snapshot

import cv2
from PyQt5.QtWidgets import QLabel
import numpy as np

from  resource import Resource 

class Camera(Resource):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.falsy_data = None
        self.update_cur_data()
        self.img_label = None
        self._scaling_factor = 1
    
    def set_label(self, img_label: QLabel):
        self.img_label = img_label

    def get_cur_data_factor(self) -> float:
        return self.cur_data.shape[1] / self.cur_data.shape[0]

    def update_scaling_factor(self):
        width = self.img_label.width()
        height = self.img_label.height()
        label_factor = width/height
        cur_data_factor = self.get_cur_data_factor()
        scaling_factor = (width / self.cur_data.shape[1] \
            if cur_data_factor > label_factor else height / self.cur_data.shape[0])
        self._scaling_factor = scaling_factor

    def update_cur_data(self):
        success, orig_img_bgr = self.cap.read()                        
        if not success:
            # Не удалось захватить изображение
            # Здесь нужно вернуть изображение с информацией об ошибке
            self.cur_data = self.falsy_data
        orig_img = cv2.cvtColor(orig_img_bgr, cv2.COLOR_BGR2RGB)
        self.cur_data = orig_img

    def get_viz_shape(self) -> list[int]:
        return list(
            map(lambda x: round(x*self._scaling_factor),
                self.cur_data.shape[:2][::-1]))

    @property
    def visualization(self):
        viz = cv2.resize(self.cur_data, self.get_viz_shape())
        return cv2.cvtColor(viz, cv2.COLOR_RGB2RGBA)