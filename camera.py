# from tracemalloc import Snapshot
from typing import List

import cv2
from PyQt5.QtWidgets import QLabel

from  resource import Resource


class Camera(Resource):
    """
    Захватывает изображение из видеопотока в поле cur_data
    и представляет доступ к этому полю.
    """
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.falsy_data = None
        self.update_cur_data()
        self.img_label = None
        self._scaling_factor = 1.0
        self.viz_shape = self.cur_data.shape[:2][::-1]
    
    def update_cur_data(self):
        success, orig_img_bgr = self.cap.read()                        
        if not success:
            # Не удалось захватить изображение
            # Здесь нужно вернуть изображение с информацией об ошибке.
            # Тогда и пользователь узнает о проблеме
            # и падать ничего точно не будет.
            self.cur_data = self.falsy_data
            print("Couldn't access the camera. Do you have it? " \
                "Is it used by another program?")
            return
        orig_img = cv2.cvtColor(orig_img_bgr, cv2.COLOR_BGR2RGB)
        self.cur_data = orig_img

    @property
    def visualization(self):
        viz = cv2.resize(self.cur_data, self.get_viz_shape())
        # print(f"{viz.shape}")
        return cv2.cvtColor(viz, cv2.COLOR_RGB2RGBA)

    """
    Все методы ниже необходимы для корректного масштабирования 
    Camera.visualization и визуализаций сенсоров, накладывющихся поверх
    визуализации камеры.
    """
    def set_label(self, img_label: QLabel):
        """
        Устанавливает в поле img_label QLabel,
        в который Visalizer будет вносить собранное изображение.
        """
        self.img_label = img_label

    def get_cur_data_wh_ratio(self) -> float:
        """Отношение ширины к высоте в исходном изображении с камеры"""
        return self.cur_data.shape[1] / self.cur_data.shape[0]

    def update_scaling_factor(self):
        label_width = self.img_label.width()
        label_height = self.img_label.height()
        label_wh_ratio = label_width / label_height
        cur_data_wh_ratio = self.get_cur_data_wh_ratio()

        if label_wh_ratio > cur_data_wh_ratio:
            scaling_factor = label_width / self.cur_data.shape[1]
        else:
            scaling_factor = label_height / self.cur_data.shape[0]

        # if scaling_factor < 0.2:
        #     scaling_factor = 1.0

        self._scaling_factor = scaling_factor
        self.update_viz_shape()


    def update_viz_shape(self):
        self.viz_shape = list(
            map(lambda x: round(x*self._scaling_factor),
                self.cur_data.shape[:2][::-1]))

    def get_viz_shape(self) -> List[int]:
        """Возвращает список [ширина, высота]"""
        return self.viz_shape