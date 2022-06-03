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
                 resource: Camera, min_possible: float, max_possible: float,
                 model_dir: str, weights_dir: str,
                 model_name: str = 'fer.json',
                 weights_name: str = 'fer.h5') -> None:

        super().__init__(names, icon_locations,
                         resource, min_possible, max_possible)
        self._model = FerSensor._load_nn(
            model_dir, weights_dir, model_name, weights_name)
        self._detect_faces = FerSensor._get_face_detetctor()
        self._face_coords = None

        # В случае FerSensor visualization - это квадратик вокруг лица
        # и прямоугольник с подписью наиболее вероятной эмоции над ним.
        self.visualization = FerSensor.get_dark_overlay(
            self.resource.get_viz_shape()[::-1])    

    def _get_face_detetctor():
        """
        Эта функция — обертка. Она возвращает функцию detect_faces.
        Если потребуется поменять детектор, будет меняться только код
        get_face_detetctor. Таким образом, будет легче поддерживать код.
        """
        face_detector = cv2.CascadeClassifier(
            r'haarcascade_frontalface_default.xml')
        def detect_faces(img):
            """
            Возвращает координаты (x, y, w, h) для каждого обнаруженного лица.
            """
            return face_detector.detectMultiScale(img, 1.32, 5)
        return detect_faces

    def get_results(self, input):
        results = self._model.predict(input)[0]
        self.visualize_prediction(results)
        return results
    
    def _get_rect_area(rect):
        _,_,w,h = rect
        return w*h

    def detect_largest_face(self, img) -> tuple[int]:
        """
        Возвращает координаты (x, y, w, h) самого большого лица на img.
        """
        # Поместив этот блок до и после детектора,
        # можно отследить, сколько ресусов затрачивает детектор
        # self.visualization = FerSensor.get_dark_overlay(
        #         self.resource.get_viz_shape()[::-1])
        # return None

        all_faces_rects = self._detect_faces(img)

        if len(all_faces_rects) == 0:
            # сбросим визуализацию. Иначе будет рендериться старая рамка
            self.visualization = FerSensor.get_dark_overlay(
                self.resource.get_viz_shape()[::-1])
            return None
        
        # Для распознавания используется самое большое лицо:
        # предполагается, что польователь будет находиться ближе всех к камере
        largest_face_rect = max(all_faces_rects, key=FerSensor._get_rect_area)
        return largest_face_rect

    def face_img_to_nn_input(face_img):
        """
        Подготовливает изображение лица к формату входных данных нейронной сети
        """
        gray_face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        gray_face_48 =cv2.resize(gray_face_img,(48,48))

        gray_face_48_normed = gray_face_48 / 255

        # добавляем размерность, отвечающую за число каналов. (48, 48, 1)
        nn_input = np.expand_dims(gray_face_48_normed, axis = 2)

        # добавляем размерность, отвечющую за число элементов батча.
        # (1, 48, 48, 1) 
        nn_input = np.expand_dims(nn_input, axis = 0)
        return nn_input

    def preprocess(self, cam_img):
        """
        Предобработка: от исходного изображения с камеры
        до изображения самого большого лица,
        подготовленного стать входом нейронной сети
        """
        largest_face_rect = self.detect_largest_face(cam_img)
        if largest_face_rect is None:
            return None

        (x,y,w,h) = self._face_coords = largest_face_rect 
        
        face_img = cam_img[y:y+h, x:x+w]

        nn_input = FerSensor.face_img_to_nn_input(face_img)

        self.init_viz_with_detection(self.resource.get_viz_shape()[::-1], largest_face_rect)

        return nn_input
    
    def _load_nn(model_dir, weights_dir,
                 model_name = 'fer.json', weights_name = 'fer.h5'):
        """Загрузка нейронной сети, распознающей эмоции."""
        # загрузим модель
        model = model_from_json(open(os.path.join(model_dir, model_name), "r").read())
        # загрузим веса
        model.load_weights(os.path.join(model_dir, weights_dir, weights_name))
        return model
    

    def get_dark_overlay(img_height_and_width: tuple[int],
                         rgba_color: tuple[int] = None) -> np.ndarray:
        """
        Получение RGBA изображения размером img_height_and_width
        в виде np.ndarray с затемнением цвета rgba_color.
        """
        if rgba_color is None:
            rgba_color = FerSensor.vis_colors['dark_overlay']
        rgba_layers = []
        for channel_val in rgba_color:
            rgba_layers.append(
                np.full(img_height_and_width, channel_val, dtype=np.uint8))
        dark_overlay = np.dstack(rgba_layers)
        return dark_overlay 

    def init_viz_with_detection(self, img_height_and_width, face_coords):
        """
        Инициализация визуализации в виде добавления рамочки вокруг лица,
        поля для текста над рамочкой и затеменения всего вне рамочки.
        """
        visualisation = FerSensor.get_dark_overlay(img_height_and_width)

        # print(f"{img_height_and_width =}")
        # print(f"{(self.resource.img_label.width(), self.resource.img_label.height()) = }")
        # print(f"{self.resource._scaling_factor = }")

        # (x,y,w,h) = face_coords

        s_x, s_y, s_w, s_h = [
            round(coord * self.resource._scaling_factor)
            for coord in face_coords]

        # print(f"{face_coords = }")
        # print(f"{transparent_img[s_y:s_y+s_h, s_x:s_x+s_w, 3].shape = }")
        
        # Сделаем участок с лицом прозрачным
        visualisation[s_y:s_y+s_h, s_x:s_x+s_w, 3] = np.zeros(
            (s_w, s_h), dtype=np.uint8)

        # Добавим рамку вокруг лица
        cv2.rectangle(
            visualisation, (s_x,s_y), (s_x+s_w,s_y+s_h),
            self.vis_colors['frame'], thickness=4)

        font_height = 20
        font_padding_vertical = 3

        # создадим контур и заливку рамки для текста
        cv2.rectangle(
            visualisation,
            (s_x,s_y),
            (s_x + s_w, s_y - font_height - font_padding_vertical*2),
            self.vis_colors['frame'],
            thickness=-1,)
        
        cv2.rectangle(
            visualisation,
            (s_x,s_y),
            (s_x + s_w, s_y - font_height - font_padding_vertical*2),
            self.vis_colors['frame'],
            thickness=4,)

        self.visualization = visualisation


    def visualize_prediction(self, results):
        """
        Добавление в поле для текста на визуализации текста
        с наиболее вероятной эмоцией и ее вероятностью.
        """
        font_height = 20
        font_padding_vertical = 3
        font_padding_horizontal = 10

        # (x,y,_,_) = self._face_coords
        s_x, s_y = [
            round(coord * self.resource._scaling_factor)
            for coord in self._face_coords[:2]]

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
            font = font, fill = self.vis_colors['text'])
        self.visualization = np.array(img_pil)
        # cv2.imshow('window_name', self.visualization)


    vis_colors = {
        'dark_overlay': (19, 20, 22, 91),
        'frame': (23, 33, 43, 255),
        'text': (255, 255, 255, 255)}


icons_dir = 'icons/emojis/'
emotions = [
    "angry", "disgusted", "fearful", "happy", "sad", "surprised", "neutral"]

emotions_icons = [
    os.path.join(icons_dir, f"{emotion}.svg") for emotion in emotions]

# model_dir = 'models/KMUnet/KmuNet_drop_0.5_01_06_2022_18_19_not_centered/'
# model_dir = 'models/KMUnet/02_06_22_mod3'
model_dir = 'models/KMUnet/02_06_22_mod11'
model_weights_dir = '2'