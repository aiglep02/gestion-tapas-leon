from abc import ABC, abstractmethod

class IEstrategiaEstadistica(ABC):
    @abstractmethod
    def calcular(self, tapas):
        pass