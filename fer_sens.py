import os

import cv2
from tensorflow.keras.models import model_from_json 
# ! удалить # from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

from sensor import SensorWithVisual


class FerSensor(SensorWithVisual):
    """
    В случае FerSensor visualization - это квадратик
    вокруг лица распознаваемого человека
    и прямоугольник с подписью наиболее вероятной эмоции над ним
    """
    def __init__(self, names, icon_locations,
                 resource, min_possible, max_possible,
                 dir_, model_name = 'fer.json', weights_name = 'fer.h5'):
        super().__init__(names, icon_locations,
                         resource, min_possible, max_possible)
        self._model = FerSensor._load_nn(dir_, model_name, weights_name)
        self._face_detector = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

    def get_results(self):
        return self._model.predict()
        
    def _get_rect_area(rect):
        _,_,w,h = rect
        return w*h


    def preprocess(self, cam_img):
        all_faces_rects = self._face_detector.detectMultiScale(cam_img, 1.32, 5)

        if len(all_faces_rects) == 0:
            return None
        
        # Для распознавания используется самое большое лицо:
        # предполагается, что польователь будет находиться ближе всех к камере
        largest_face_rect = max(all_faces_rects, key=FerSensor._get_rect_area)
        
        (x,y,w,h) = largest_face_rect
        
        # cv2.imshow('f', face_img)
        face_img = cam_img[y:y+h, x:x+w]
        gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        cut_gray_face =cv2.resize(gray_face_img,(48,48))

        # ! Два комментария ниже убрать
        # добавляет канал в конец. Те размерность (48, 48, 1)
        # ar = img_to_array(cut_gray_face)

        cut_gray_face_normed = cut_gray_face / 255

        # добавляем размерность, отвечющую за число каналов. (48, 48, 1)
        nn_input = np.expand_dims(cut_gray_face_normed, axis = 2)

        # добавляем размерность, отвечющую за число элементов батча.
        # (1, 48, 48, 1) 
        nn_input = np.expand_dims(nn_input, axis = 0)

        print(nn_input.shape)

        chan_num = 4
        transparent_img = np.zeros(
            (cam_img.shape[0], cam_img.shape[1], chan_num), dtype=np.uint8)
        
        # выделим рамкой участок с лицом, который обработает модель
        rect_color = (114,106,106)
        cv2.rectangle(transparent_img,(x,y),(x+w,y+h),rect_color,thickness=4)

        self.visualization = transparent_img

        return nn_input
    
    def _load_nn(dir_, model_name = 'fer.json', weights_name = 'fer.h5'):
        # загрузим модель
        model = model_from_json(open(os.path.join(dir_, model_name), "r").read())
        # загрузим веса
        model.load_weights(os.path.join(dir_, weights_name))
        return model


icons_dir = 'icons/emojis/'
emotions = ["happy", "sad", "angry", "neutral", "surprised"]
emotions_icons = [os.path.join(icons_dir, f"{emotion}.svg") for emotion in emotions]
KMU_dir = 'models/KMUnet/KmuNet_drop_0.5/'

"""
fer_sens = FerSensor( 
    emotions, emotions_icons,
    load_nn(KMU_dir).predict, 0, 1)
"""