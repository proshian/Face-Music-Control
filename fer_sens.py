import os

import cv2
from tensorflow.keras.models import model_from_json 
from tensorflow.keras.preprocessing.image import img_to_array

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
        #for (x,y,w,h) in faces_detected:
        print(f"all rects {all_faces_rects}")
        if len(all_faces_rects) == 0:
            return
        largest_face_rect = max(all_faces_rects, key=FerSensor._get_rect_area)
        print(f"largest_using_max: {largest_face_rect}")
        (x,y,w,h) = largest_face_rect
        
        
        face_img = cam_img[y:y+h, x:x+w]
        # cv2.imshow('f', face_img)
        gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('f', gray_face_img)
        cut_gray_face =cv2.resize(gray_face_img,(48,48))
        # cv2.imshow('f', cv2.resize(cut_gray_face,(200,200)))
        #print(f"shape: {cut_gray_face.shape}")
        #print(f"type: {type(cut_gray_face)}")
        #print(cut_gray_face)

        # добавляет канал в конец. Те размерность (48, 48, 1)
        ar = img_to_array(cut_gray_face)
        
        #print(f"ar shape: {ar.shape}")
        #print(f"ar type: {type(ar)}")
        #print(ar)
    
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