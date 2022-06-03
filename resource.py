import itertools
from abc import ABC, abstractmethod


class Resource():
    """
    Предоставляет исходные данные для объектов наследников класса Sensor.
    Умеет обновлять поле cur_data c помощью метода update_cur_data и 
    предоставлять доступ к этому полю с помощью get_cur_data.
    """
    id_iterator = itertools.count()

    all_resources = []
    def __init__(self) -> None:
        self.id: int = next(Resource.id_iterator)
        self.cur_data = None
        # Нужно определить в наследнике falsy_data - данные,
        # сведетельствующие об ошибке
        self.falsy_data = None
        Resource.all_resources.append(self)

    @abstractmethod
    def update_cur_data(self):
        pass

    def get_cur_data(self):
        return self.cur_data