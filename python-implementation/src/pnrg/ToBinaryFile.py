from pnrg import RNG
import numpy as np


def create_binary_file(rng: RNG, rounds, round_size=80000, filepath="./", filename=None):
    if filename is None:
        filename = rng.get_name()

    f = None
    try:
        f = open(filepath + filename, "bw+", round_size)
    except IOError as ex:
        print("Couldn't create file: " + str(ex))
        exit(1)

    for i in range(rounds):
        buffer = bytearray(round_size)
        for j in range(0, round_size, 8):
            out = int(rng.next_64_bits()).to_bytes(8, byteorder='little', signed=True)
            for k in range(8):
                buffer[i + k] = out[k]
        f.write(buffer)




