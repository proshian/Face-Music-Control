from abc import ABC, abstractmethod

class PartialVizualizationCreator(ABC):

    @abstractmethod
    def get_vizualization(self):
        pass
    