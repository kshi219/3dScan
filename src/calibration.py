import yaml
import numpy as np


PATH = '/home/kevin/Desktop/learningResources/3dscan/cartman-calib/calibration.yml'

class Calib():

    def __init__(self, path=PATH):
        self.file = path
        stream = file(self.file, 'r')
        calib_vars_dict = yaml.load(stream)
        self.R = self.raw2arr(calib_vars_dict, 'R')
        self.Rt = np.transpose(self.R)
        self.T = self.raw2arr(calib_vars_dict, 'T')
        self.cam_K = self.raw2arr(calib_vars_dict, 'cam_K')
        self.cam_Kc = self.raw2arr(calib_vars_dict, 'cam_kc')
        self.proj_K = self.raw2arr(calib_vars_dict, 'proj_K')
        self.proj_Kc = self.raw2arr(calib_vars_dict, 'proj_kc')

    def raw2arr(self, raw, var):
        data = raw[var]['data']
        rows = raw[var]['rows']
        cols = raw[var]['cols']
        ret = np.reshape(data, (rows, cols))
        return ret









