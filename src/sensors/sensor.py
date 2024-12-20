import itertools
from abc import ABC, abstractmethod


class Sensor(ABC):
    """
    Метод get_results объектоы наследников Sensor возвращает массив float'ов,
    в соответствии с которыми мы хотим управлять звучанием  
    """
    id_iterator = itertools.count()

    def __init__(self, names, icon_locations,
                 resource, min_possible, max_possible):

        self.names = names
        self.icon_locations = icon_locations
        self.min_possible = min_possible
        self.max_possible = max_possible
        self.resource = resource
        
        self.id = next(Sensor.id_iterator)

    def acquire_raw(self):
        return self.resource.get_cur_data()
    
    @abstractmethod
    def get_results_from_raw(self, raw_data):
        pass
