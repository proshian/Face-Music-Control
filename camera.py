from tracemalloc import Snapshot


import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    def update_snapshot(self):
        success, orig_img_bgr = self.cap.read()                        
        if not success:
            # Не удалось захватить изображение
            # Здесь нужно вернуть изображение с информацией об ошибке
            return
        orig_img = cv2.cvtColor(orig_img_bgr, cv2.COLOR_BGR2RGB)
        self.snapshot = orig_img
