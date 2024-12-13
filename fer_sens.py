import os
from typing import List, Tuple

import cv2
from tensorflow.keras.models import model_from_json 
import numpy as np

from sensor import Sensor
from camera import Camera
from face_detector import face_detector


class FerSensor(Sensor):
    """
    Метод get_results возвращает массив вероятностей семи эмоций,
    названия которых представлены в поле names
    """
    def __init__(self, names: List[str], icon_locations: List[str],
                 resource: Camera, min_possible: float, max_possible: float,
                 model_dir: str, weights_dir: str,
                 model_name: str = 'fer.json',
                 weights_name: str = 'fer.h5') -> None:

        super().__init__(names, icon_locations,
                         resource, min_possible, max_possible)
        self._model = FerSensor._load_nn(
            model_dir, weights_dir, model_name, weights_name)
        self.face_detector = face_detector
        self.cur_largest_face_rect = None
        self.cur_results = None
        
    def get_results_from_raw(self, raw_data):
        nn_input = self.preprocess(raw_data)
        if nn_input is None:
            self.cur_results = None
        else:
            self.cur_results = self._model.predict(nn_input)[0]
        return self.cur_results

    def face_img_to_nn_input(face_img: np.ndarray) -> List[float]:
        """
        Подготовка изображения лица к формату входных данных нейронной сети
        """
        gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        gray_face_48 = cv2.resize(gray_face_img,(48,48))
        gray_face_48_normed = gray_face_48 / 255
        # Add dimensions for channels and batch size (1, 48, 48, 1).
        nn_input = np.expand_dims(gray_face_48_normed, axis = (0, 3))        
        return nn_input

    def preprocess(self, cam_img):
        """
        Предобработка: от исходного изображения с камеры
        до изображения самого большого лица,
        подготовленного стать входом нейронной сети
        """
        # The emotions are recognized on largest detected face.
        # It's supposed that the user is the closest person to the camera.
        largest_face_rect = self.face_detector.detect_largest_face(cam_img)
        if largest_face_rect is None:
            self.cur_largest_face_rect = None
            return None

        (x,y,w,h) = self.cur_largest_face_rect = largest_face_rect 
        face_img = cam_img[y:y+h, x:x+w]
        nn_input = FerSensor.face_img_to_nn_input(face_img)
        return nn_input
    
    def _load_nn(model_dir: str, weights_dir: str,
                 model_name: str = 'fer.json', weights_name: str = 'fer.h5'):
        """Загрузка нейронной сети, распознающей эмоции."""
        model = model_from_json(
            open(os.path.join(model_dir, model_name), "r").read())
        model.load_weights(os.path.join(model_dir, weights_dir, weights_name))
        return model
  

icons_dir = 'icons/emojis/'

# задание преобразований из чисел в эмоции и наоборот
emotions = ('happy', 'sad', 'angry', 'neutral', 'surprised', 'fearful')
# emotion_dict = {emotions[i] : i for i in range(len(emotions))}


emotions_icons = [
    os.path.join(icons_dir, f"{emotion}.svg") for emotion in emotions]

model_dir = 'models/FerPLUS_6_emotions/mod2/'
model_weights_dir = '1'




# Values below are alternatives to the ones above. They use KMUnet trained on FER2013

# emotions = [
#     "angry", "disgusted", "fearful", "happy", "sad", "surprised", "neutral"]

# model_dir = 'models/KMUnet/KmuNet_drop_0.5_01_06_2022_18_19_not_centered/'
# # model_dir = 'models/KMUnet/02_06_22_mod3'
# # model_dir = 'models/KMUnet/02_06_22_mod11'
# model_weights_dir = '1'