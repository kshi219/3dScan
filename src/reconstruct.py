import numpy as np
from calibration import Calib
from decode import Decoder


class reconstruct():
    def __init__(self):
        self.decoded = Decoder()
        self.calib = Calib()
