from abc import ABC, abstractmethod

class PartialVisualizationCreator(ABC):
    @abstractmethod
    def get_vizualization(self):
        pass
    