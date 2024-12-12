from typing import Optional
from abc import ABC, abstractmethod

import cv2
import numpy as np
import mediapipe as mp

from typing import List, Tuple
"""
Предполагается, что несколько сенсоров могут требовать детекции лица.
Кажется логичным создать один объект детектора
и включать его в каждый из сенсоров.
"""


class FaceDetector(ABC):
    """
    Отвечает за детекцию лиц, в частности, самого большого лица.
    """
    @abstractmethod
    def detect_faces(self, img: np.ndarray) -> List[Tuple[int]]:
        pass

    def _box_in_boundaries(detection_tuple: Tuple[int],
                           img_h: int, img_w: int) -> bool:
        x, y, w, h = detection_tuple
        return (x > 0) and (y > 0) and (x+w < img_w) and (y+h < img_h)


    def _get_rect_area(rect: Tuple[int]) -> int:
        _,_,w,h = rect
        return w*h

    def detect_largest_face(self, img: np.ndarray) -> Optional[np.ndarray]:
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



class MpFaceDetector(FaceDetector):
    def __init__(self) -> None:
        mp_face_detection = mp.solutions.face_detection
        self.mp_face_detection = mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.7)
    
    def detect_faces(self, img: np.ndarray) -> List[Tuple[int]]:
        mp_results = self.mp_face_detection.process(img)
        mp_detections = []
        if mp_results.detections:
            for result in mp_results.detections:
                box = result.location_data.relative_bounding_box
                img_h, img_w = img.shape[0], img.shape[1]
                detection_tuple = MpFaceDetector._mediapipe_bo_to_tuple(
                    box, img_h, img_w)
                    
                if MpFaceDetector._box_in_boundaries(
                        detection_tuple, img_h, img_w):
                    mp_detections.append(detection_tuple)
        return mp_detections

    def _mediapipe_bo_to_tuple(box, img_h: int, img_w: int):
        detection_tuple_float = (
            box.xmin * img_w,
            box.ymin * img_h,
            box.width * img_w,
            box.height * img_h)
                
        detection_tuple = tuple(map(int, detection_tuple_float))
        return detection_tuple



class HaarFaceDetector(FaceDetector):
    def __init__(self) -> None:
        self._face_detector = cv2.CascadeClassifier(
            r'haarcascade_frontalface_default.xml')
    
    def detect_faces(self, img: np.ndarray) -> List[Tuple[int]]:
        return self._face_detector.detectMultiScale(img, 1.32, 5)


# Данный объект будет внедряться во все sensor'ы, где требуется детекция лиц
face_detector = MpFaceDetector()