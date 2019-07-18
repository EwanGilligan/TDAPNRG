from pnrg.LFSRs import *
from pnrg.hash import *
from pnrg.LCGs import *
from pnrg import FromBinaryFile
import numpy as np

seed = np.array([0xDEADEEF, 0xFEEDFACECAFEBEEF, 0xD0D0CACA, 0x39109bb02acbe635])
rng = Xorshift128p(1, 2)
for i in range(100):
    print(rng.next_float())
