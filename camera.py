# from tracemalloc import Snapshot
from typing import List

import cv2

from  fmc_resource import Resource


class Camera(Resource):
    """
    Захватывает изображение из видеопотока в поле cur_data
    и представляет доступ к этому полю.
    """
    def __init__(self) -> None:
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.falsy_data = None
        self.update_cur_data()
    
    def update_cur_data(self) -> None:
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
