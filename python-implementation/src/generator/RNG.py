from abc import ABC, abstractmethod


class RNG(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def next_long(self):
        pass

    @abstractmethod
    def next_double(self):
        pass

    @abstractmethod
    def next_64_bits(self):
        pass
