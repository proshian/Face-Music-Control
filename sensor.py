import itertools

class Sensor():
    id_iterator = itertools.count()

    all_sensors = []

    def __init__(self, names, icon_locations, get_results,
                 min_possible, max_possible,
                 acquire_raw = lambda : None, preprocess = lambda x : None):

        self.names = names
        self.icon_locations = icon_locations
        self.get_results = get_results
        self.min_possible = min_possible
        self.max_possible = max_possible
        self.acquire_raw = acquire_raw
        self.preprocess = preprocess
        
        self.id = next(Sensor.id_iterator)
        Sensor.all_sensors.append(self)
