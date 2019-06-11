from abc import ABC, abstractmethod
import numpy as np


class RNG(ABC):
    def __init__(self, name: str):
        """

        :param name: Name of the Random Number Generator
        """
        self.name = name

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def next_int(self) -> np.int64:
        pass

    @abstractmethod
    def next_float(self) -> np.float64:
        pass

    @abstractmethod
    def next_64_bits(self):
        pass
