import os

import cv2
from tensorflow.keras.models import model_from_json 
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from sensor import SensorWithVisual
from camera import Camera


class FerSensor(SensorWithVisual):
    """
    Метод get_results возвращает массив вероятностей семи эмоций,
    названия которых представлены в поле names
    """
    def __init__(self, names: list[str], icon_locations: list[str],
                 resource: Camera, min_possible, max_possible, dir_: str,
                 model_name: str = 'fer.json', weights_name: str = 'fer.h5'):
        super().__init__(names, icon_locations,
                         resource, min_possible, max_possible)
        self._model = FerSensor._load_nn(dir_, model_name, weights_name)
        self._face_detector = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
        self._face_coords = None

        # В случае FerSensor visualization - это квадратик вокруг лица
        # и прямоугольник с подписью наиболее вероятной эмоции над ним.
        self.visualization = FerSensor.get_dark_overlay(
            self.resource.visualization.shape)    

    def get_results(self, input):
        results = self._model.predict(input)[0]
        self.visualize_prediction(results)
        return results
    
    def _get_rect_area(rect):
        _,_,w,h = rect
        return w*h

    def preprocess(self, cam_img):
        all_faces_rects = self._face_detector.detectMultiScale(cam_img, 1.32, 5)

        if len(all_faces_rects) == 0:
            # сбросим визуализацию. Иначе будет рендериться старая рамка
            # self.visualization = np.zeros(
            #     self.resource.visualization.shape, dtype=np.uint8)

            # решил, что лучше затемнять весь кадр
            self.visualization = FerSensor.get_dark_overlay(
                self.resource.get_viz_shape()[::-1])
                #self.resource.visualization.shape[:2])
            return None
        
        # Для распознавания используется самое большое лицо:
        # предполагается, что польователь будет находиться ближе всех к камере
        largest_face_rect = max(all_faces_rects, key=FerSensor._get_rect_area)
        self._face_coords = largest_face_rect 
        (x,y,w,h) = largest_face_rect
        
        # cv2.imshow('f', face_img)
        face_img = cam_img[y:y+h, x:x+w]
        gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        cut_gray_face =cv2.resize(gray_face_img,(48,48))

        cut_gray_face_normed = cut_gray_face / 255

        # добавляем размерность, отвечающую за число каналов. (48, 48, 1)
        nn_input = np.expand_dims(cut_gray_face_normed, axis = 2)

        # добавляем размерность, отвечющую за число элементов батча.
        # (1, 48, 48, 1) 
        nn_input = np.expand_dims(nn_input, axis = 0)


        self.init_viz_with_detection(self.resource.get_viz_shape()[::-1], largest_face_rect)

        return nn_input
    
    def _load_nn(dir_, model_name = 'fer.json', weights_name = 'fer.h5'):
        # загрузим модель
        model = model_from_json(open(os.path.join(dir_, model_name), "r").read())
        # загрузим веса
        model.load_weights(os.path.join(dir_, weights_name))
        return model
    

    def get_dark_overlay(img_height_and_width,
                         rgba_color: tuple[int] = (19, 20, 22, 91)):
        rgba_layers = []
        for channel_val in rgba_color:
            rgba_layers.append(
                np.full(img_height_and_width, channel_val, dtype=np.uint8))
        transparent_img = np.dstack(rgba_layers)
        return transparent_img 

    def init_viz_with_detection(self, img_height_and_width, face_coords):
        # Затемняю фон. Также можно рассмотреть:
        #     * засветление квадрата с лицом
        #     * отсутствие затемнения или засветления
        transparent_img = FerSensor.get_dark_overlay(img_height_and_width)

        # print(f"{img_height_and_width =}")
        # print(f"{(self.resource.img_label.width(), self.resource.img_label.height()) = }")
        # print(f"{self.resource._scaling_factor = }")

        # (x,y,w,h) = face_coords

        s_x, s_y, s_w, s_h = [
            round(coord * self.resource._scaling_factor)
            for coord in face_coords]

        # print(f"{face_coords = }")
        # print(f"{transparent_img[s_y:s_y+s_h, s_x:s_x+s_w, 3].shape = }")
        
        face_frame_color = (23, 33, 43, 255)

        # Сделаем участок с лицом прозрачным
        transparent_img[s_y:s_y+s_h, s_x:s_x+s_w, 3] = np.zeros(
            (s_w, s_h), dtype=np.uint8)

        cv2.rectangle(
            transparent_img, (s_x,s_y), (s_x+s_w,s_y+s_h), face_frame_color, thickness=4)

        font_height = 20
        font_padding = 3

        # создадим контур и заливку рамки для текста
        cv2.rectangle(
            transparent_img, (s_x,s_y), (s_x + s_w, s_y - font_height - font_padding*2),
            face_frame_color, thickness=-1)
        
        cv2.rectangle(
            transparent_img, (s_x,s_y), (s_x + s_w, s_y - font_height - font_padding*2),
            face_frame_color, thickness=4)

        self.visualization = transparent_img


    def visualize_prediction(self, results):
        font_height = 20
        font_padding_vertical = 3
        font_padding_horizontal = 10

        # (x,y,_,_) = self._face_coords
        # ! PEP8!
        s_x, s_y = [round(coord * self.resource._scaling_factor) for coord in self._face_coords[:2]] 

        max_index = np.argmax(results)  # номер наиболее вероятной эмоции
    
        predicted_emotion = self.names[max_index]  # наиболее вероятная эмоция        
        font = ImageFont.truetype("arial.ttf", font_height)
        img_pil = Image.fromarray(self.visualization)
        draw = ImageDraw.Draw(img_pil)
        text_coords = (int(s_x + font_padding_horizontal),
                       int(s_y - font_height - font_padding_vertical))
        draw.text(
            text_coords,
            f"{predicted_emotion}  {results[max_index]*100:.0f}%",
            font = font, fill = (255, 255, 255, 255))
        self.visualization = np.array(img_pil)
        # cv2.imshow('f', self.visualization)


icons_dir = 'icons/emojis/'
emotions = [
    "angry", "disgusted", "fearful", "happy", "sad", "surprised", "neutral"]

emotions_icons = [
    os.path.join(icons_dir, f"{emotion}.svg") for emotion in emotions]

KMU_dir = 'models/KMUnet/KmuNet_drop_0.5_01_06_2022_18_19_not_centered/'