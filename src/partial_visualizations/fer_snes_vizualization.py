from typing import Tuple

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from .camera_vizualization import CameraPartialVizualizationCreator
from sensors.fer_sens import FerSensor
from .partial_vizualization_creator import PartialVizualizationCreator



class FerSensorPartialVizualizationCreator(PartialVizualizationCreator):
    """
    Метод get_results возвращает массив вероятностей семи эмоций,
    названия которых представлены в поле names
    """
    def __init__(self, fer_sensor: FerSensor, camera_vizalization: CameraPartialVizualizationCreator) -> None:

        # В случае FerSensor visualization - это квадратик вокруг лица
        # и прямоугольник с подписью наиболее вероятной эмоции над ним.
        self.fer_sensor = fer_sensor
        self.camera_vizalization = camera_vizalization
        self.visualization = FerSensorPartialVizualizationCreator.get_dark_overlay(
            self.camera_vizalization.get_viz_shape()[::-1])


    def get_vizualization(self):
        if self.fer_sensor.cur_results is None or self.fer_sensor.cur_largest_face_rect is None:
            self.visualization = FerSensorPartialVizualizationCreator.get_dark_overlay(
                self.camera_vizalization.get_viz_shape()[::-1])
            return self.visualization
        largest_face_bounding_box = self.fer_sensor.cur_largest_face_rect
        self.init_viz_with_detection(self.camera_vizalization.get_viz_shape()[::-1], 
                                     largest_face_bounding_box)
        self.add_prediction_field_to_vizalization(self.fer_sensor.cur_results)
        return self.visualization
        

    def get_dark_overlay(img_height_and_width: Tuple[int],
                         rgba_color: Tuple[int] = None) -> np.ndarray:
        """
        Получение RGBA изображения размером img_height_and_width
        в виде np.ndarray с затемнением цвета rgba_color.
        """
        if rgba_color is None:
            rgba_color = FerSensorPartialVizualizationCreator.vis_colors['dark_overlay']
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
        Внутренность рамочки прозрачная.
        """
        visualisation = FerSensorPartialVizualizationCreator.get_dark_overlay(img_height_and_width)

        s_x, s_y, s_w, s_h = [
            round(coord * self.camera_vizalization._scaling_factor)
            for coord in face_coords]
        
        # Сделаем участок с лицом прозрачным
        visualisation[s_y:s_y+s_h, s_x:s_x+s_w, 3] = np.zeros(
            (s_h, s_w), dtype=np.uint8)

        # Добавим рамку вокруг лица
        cv2.rectangle(
            visualisation, (s_x,s_y), (s_x+s_w,s_y+s_h),
            self.vis_colors['frame'], thickness=4)

        # создадим заливку рамки для текста
        cv2.rectangle(
            visualisation, (s_x,s_y),
            (s_x + s_w,
                s_y - self.FONT_HEIGHT - self.FONT_PADDING_VERTICAL*2),
            self.vis_colors['frame'], thickness=-1,)
        
        # создадим контур рамки для текста
        cv2.rectangle(
            visualisation, (s_x,s_y),
            (s_x + s_w,
                s_y - self.FONT_HEIGHT - self.FONT_PADDING_VERTICAL*2),
            self.vis_colors['frame'], thickness=4,)

        self.visualization = visualisation


    def add_prediction_field_to_vizalization(self, results):
        """
        Добавление в поле для текста на визуализации текста
        с наиболее вероятной эмоцией и ее вероятностью.
        """
        s_x, s_y = [
            round(coord * self.camera_vizalization._scaling_factor)
            for coord in self.fer_sensor.cur_largest_face_rect[:2]]

        max_index = np.argmax(results)  # номер наиболее вероятной эмоции
    
        predicted_emotion = self.fer_sensor.names[max_index]  # наиболее вероятная эмоция 
        font = ImageFont.truetype("arial.ttf", self.FONT_HEIGHT)
        img_pil = Image.fromarray(self.visualization)
        draw = ImageDraw.Draw(img_pil)
        text_coords = (
            int(s_x + self.FONT_PADDING_HORIZONTAL),
            int(s_y - self.FONT_HEIGHT - self.FONT_PADDING_VERTICAL))
        draw.text(
            text_coords,
            f"{predicted_emotion}  {results[max_index]*100:.0f}%",
            font = font, fill = self.vis_colors['text'])
        self.visualization = np.array(img_pil)


    vis_colors = {
        'dark_overlay': (19, 20, 22, 91),
        'frame': (23, 33, 43, 255),
        'text': (255, 255, 255, 255)}
    
    # Параметры текста с наиболее веротяной эмоцией, помещаемого над лицом.
    FONT_HEIGHT = 20
    FONT_PADDING_VERTICAL = 3
    FONT_PADDING_HORIZONTAL = 10
