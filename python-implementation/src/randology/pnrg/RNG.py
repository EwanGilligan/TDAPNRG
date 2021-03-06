from abc import ABC, abstractmethod
import numpy as np


class RNG(ABC):
    def __init__(self, name: str):
        """

        :param name: Name of the Random Number Generator
        """
        self.name = name

    def get_name(self) -> str:
        """
        returns the name of the random number pnrg.

        :rtype: str
        :return: string of the name.
        """
        return self.name

    @abstractmethod
    def next_int(self) -> np.int64:
        """
        Generates a random 64 bit integer.

        :rtype: np.int64
        :return: the next random 64 bit integer.
        """
        pass

    @abstractmethod
    def next_float(self) -> np.float64:
        """
        Generates a random floating point number in the range [0,1]

        :rtype: np.float64
        :return: next random float in the interval [0,1]

        """
        pass

    @abstractmethod
    def next_64_bits(self) -> np.int64:
        """
        Generates a 64 bit long random bit string

        :rtype: np.int64
        :return: 64 bit random bit string.
        """
        pass

    def next_high_order(self, k):
        """
        Return the k high order bits of the output.
        :param k: How many high order bits to take.
        :return:
        """
        return np.uint64(self.next_64_bits()) >> np.uint64(64 - k)

    def next_low_order(self, k):
        """
        Return the k low order bits of the next output.
        :param k: How many low order bits to take.
        :return:
        """
        n = np.uint64(64 - k)
        return np.uint64(self.next_64_bits()) << n >> n

