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

    def detection_visualize(orig_img, coords):
        (x,y,w,h) = coords
        cv2.rectangle(orig_img,(x,y),(x+w,y+h),(114,106,106),thickness=4)

        font_height = 20
        font_padding = 3

        # создадим контур и заливку рамки для текста
        cv2.rectangle(
            orig_img,(x,y),(x+w,y-font_height-font_padding * 2),(114,106,106),thickness=-1)
        
        cv2.rectangle(
            orig_img,(x,y),(x+w,y-font_height-font_padding * 2),(114,106,106),thickness=4)

        """
        # Наложим поверх найденного лица полупрозрачную маску:
        # 1) Запишем часть, содержащую лицо в паеременную sub_img
        sub_img = orig_img[y:y+h, x:x+w]

        # 2) Создадим белый квадрат такого же размера, как sub_img
        white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255

        # 3) Сложим лицо с белым квадратом с коффицинтами 0.9 и 0.1
        res = cv2.addWeighted(sub_img, 0.85, white_rect, 0.15, 1.0)

        # 4) Перезапишим участок с лицом на "приглушенную версию"
        orig_img[y:y+h, x:x+w] = res
        """
        return orig_img

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





        n_channels = 4
        """
        transparent_img = np.zeros(
            (cam_img.shape[0], cam_img.shape[1], n_channels), dtype=np.uint8)
        """
        
        transparent_img = np.ones(
            (cam_img.shape[0], cam_img.shape[1], n_channels), dtype=np.uint8)
        transparent_img *= 255
        transparent_img[:,:,3] = np.zeros(
            (cam_img.shape[0], cam_img.shape[1]), dtype=np.uint8)

        """
        FerSensor.detection_visualize(
            transparent_img, largest_face_rect)
        """
        

        cv2.rectangle(transparent_img,(x,y),(x+w,y+h),(114,106,106,255),thickness=4)
        cv2.imshow('trans', transparent_img)

        orig_con = np.copy(cam_img)
        orig_con = cv2.cvtColor(orig_con, cv2.COLOR_RGB2RGBA)


        orig_con[transparent_img[:,:,3] != 0] = transparent_img[transparent_img[:,:,3] != 0]
        cv2.imshow('orig_con', orig_con)

        viz = FerSensor.detection_visualize(
            np.copy(cam_img), largest_face_rect)
        cv2.imshow('f', viz)


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