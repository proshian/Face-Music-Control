import itertools
from abc import ABC, abstractmethod

class Resource(ABC):
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