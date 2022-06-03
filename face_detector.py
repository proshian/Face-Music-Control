import cv2
import numpy as np


"""
Предполагается, что несколько сенсоров могут требовать детекции лица.
Кажется логичным создать один обхект детектора и включать его в каждый из сенсоров.
"""

class FaceDetector:
    """
    Отвечает за детекцию лиц, в частности, самого большого лица.
    """
    def __init__(self) -> None:
        self._face_detector = cv2.CascadeClassifier(
            r'haarcascade_frontalface_default.xml')
    
    def detect_faces(self, img: np.ndarray) -> list[tuple[int]]:
        return self._face_detector.detectMultiScale(img, 1.32, 5)

    def _get_rect_area(rect: tuple[int]) -> int:
        _,_,w,h = rect
        return w*h

    def detect_largest_face(self, img: np.ndarray) -> np.ndarray:
        """
        Возвращает координаты (x, y, w, h) самого большого лица на img.
        """
        all_faces_rects = self.detect_faces(img)

        # len в качестве проверки на пустоту,
        # потому что если лиц не было найдено, возврвщается tuple,
        # а если найдены — np.ndarray
        if len(all_faces_rects) == 0:
            return None
        
        largest_face_rect = max(all_faces_rects, key=FaceDetector._get_rect_area)
        return largest_face_rect


# Данный объект будет внедряться во все sensor'ы, где требуется детекция лиц
face_detector = FaceDetector()