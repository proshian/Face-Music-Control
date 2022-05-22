import itertools
from abc import ABC, abstractmethod

class Sensor(ABC):
    id_iterator = itertools.count()

    all_sensors = []

    def __init__(self, names, icon_locations, get_results,
                 resource, min_possible, max_possible):

        self.names = names
        self.icon_locations = icon_locations
        self.get_results = get_results
        self.min_possible = min_possible
        self.max_possible = max_possible
        self.resource = resource
        
        self.id = next(Sensor.id_iterator)
        Sensor.all_sensors.append(self)

    def acquire_raw(self):
        return self.resource.get_data()

    @abstractmethod
    def preprocess(delf):
        pass
    
