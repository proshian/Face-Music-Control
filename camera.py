# from tracemalloc import Snapshot

import cv2

from  resource import Resource 

class Camera(Resource):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.falsy_data = None
        self.update_cur_data()
    
    def update_cur_data(self):
        success, orig_img_bgr = self.cap.read()                        
        if not success:
            # Не удалось захватить изображение
            # Здесь нужно вернуть изображение с информацией об ошибке
            self.cur_data = self.falsy_data
        orig_img = cv2.cvtColor(orig_img_bgr, cv2.COLOR_BGR2RGB)
        self.cur_data = orig_img

    @property
    def visualization(self):
        return self.cur_data