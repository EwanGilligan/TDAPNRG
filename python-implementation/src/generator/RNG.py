from abc import ABC, abstractmethod


class RNG(ABC):
    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        return self.name

    @abstractmethod
    def next_long(self):
        pass

    @abstractmethod
    def next_double(self):
        pass

    @abstractmethod
    def next_64_bits(self):
        pass
