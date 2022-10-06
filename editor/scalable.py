from abc import ABC, abstractmethod


class Scalable(ABC):
    @abstractmethod
    def rescale(self, scale: float):
        ...
