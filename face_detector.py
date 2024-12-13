from typing import Optional
from abc import ABC, abstractmethod

import cv2
import numpy as np
import mediapipe as mp

from typing import List, Tuple, NamedTuple
"""
Предполагается, что несколько сенсоров могут требовать детекции лица.
Кажется логичным создать один объект детектора
и включать его в каждый из сенсоров.
"""


class BoundingBox(NamedTuple):
    x: int
    y: int
    w: int
    h: int


class FaceDetector(ABC):
    """
    Отвечает за детекцию лиц, в частности, самого большого лица.
    """
    @abstractmethod
    def detect_faces(self, img: np.ndarray) -> List[BoundingBox]:
        pass

    def _box_in_boundaries(detection_tuple: BoundingBox,
                           img_h: int, img_w: int) -> bool:
        x, y, w, h = detection_tuple
        return (x > 0) and (y > 0) and (x+w < img_w) and (y+h < img_h)

    def _get_rect_area(rect: Tuple[int]) -> int:
        _,_,w,h = rect
        return w*h

    def detect_largest_face(self, img: np.ndarray) -> Optional[BoundingBox]:
        all_faces_rects = self.detect_faces(img)

        if len(all_faces_rects) == 0:
            return None
        
        largest_face_rect = max(all_faces_rects, key=FaceDetector._get_rect_area)
        return largest_face_rect



class MpFaceDetector(FaceDetector):
    def __init__(self) -> None:
        mp_face_detection = mp.solutions.face_detection
        self.mp_face_detection = mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.7)
    
    def detect_faces(self, img: np.ndarray) -> List[BoundingBox]:
        mp_results = self.mp_face_detection.process(img)
        mp_detections = []
        # mp_results.detections is either a non-empty list or None
        if mp_results.detections:
            for result in mp_results.detections:
                box = result.location_data.relative_bounding_box
                img_h, img_w = img.shape[0], img.shape[1]
                detection_tuple = MpFaceDetector._mp_relative_box_to_bounding_box(
                    box, img_h, img_w)
                    
                if MpFaceDetector._box_in_boundaries(
                        detection_tuple, img_h, img_w):
                    mp_detections.append(detection_tuple)
        return mp_detections

    def _mp_relative_box_to_bounding_box(box, img_h: int, img_w: int) -> BoundingBox:
        detection_tuple_float = (
            box.xmin * img_w,
            box.ymin * img_h,
            box.width * img_w,
            box.height * img_h)
        
        return BoundingBox(*map(int, detection_tuple_float))


class HaarFaceDetector(FaceDetector):
    def __init__(self) -> None:
        self._face_detector = cv2.CascadeClassifier(
            r'haarcascade_frontalface_default.xml')
    
    def detect_faces(self, img: np.ndarray) -> List[BoundingBox]:
        detections: List[np.ndarray] = self._face_detector.detectMultiScale(img, 1.32, 5)
        return [BoundingBox(*detection) for detection in detections]


# Данный объект будет внедряться во все sensor'ы, где требуется детекция лиц
face_detector = MpFaceDetector()