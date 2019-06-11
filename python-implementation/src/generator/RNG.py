from abc import ABC, abstractmethod


class RNG(ABC):
    def __init__(self, name: str):
        """

        :param name: Name of the Random Number Generator
        """
        self.name = name

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def next_int(self) -> int:
        pass

    @abstractmethod
    def next_float(self) -> float:
        pass

    @abstractmethod
    def next_64_bits(self):
        pass
