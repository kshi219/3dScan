from skimage import color
from skimage import io
from glob import glob
import numpy as np
from matplotlib import pyplot as plt


ROOT_DIR = '/home/kevin/Desktop/learningResources/3dscan/cartman/'
DIRECT_EST_PARAM = 0.3
THRESH_PARAM = 0


class Decoder():
    def __init__(self, image_dir):
        self.views = glob(image_dir + '*/')
        # pattern images organized in order of least to most dense and vertical -> horizontal patterns
        self.images = sorted(glob(self.views[0] + '*.png'))
        self.size = io.imread(self.images[0]).shape[0:2]
        self.decoded_indices = np.empty(self.size + (2,), dtype=int)
        self.minmax_img = np.empty(self.size + (2,), dtype=int)
        # assuming binary gray code pattern
        self.bits  = (len(self.images)/2 - 1)/2


    def decode(self):

        # we estimate the direct and ambient sources of light using the second to last most dense pattern images

        # get images
        img1 = []
        img2 = []
        offset = self.bits*2
        start = len(self.images) - offset - 2 - 3
        for i in xrange(-1,3):
            img1.append(self.images[start + i])
            img2.append(self.images[start + i + offset])
        set_imgs =  img1 + img2
        direct_comps_img = self.direct_est(set_imgs, DIRECT_EST_PARAM)




    def direct_est(self, imgs, b):
        ret = np.empty(self.minmax_img.shape, dtype=float)
        imgs_list = []
        for i in imgs:
            img = io.imread(i, as_grey=True).astype(float)
            imgs_list.append(img)
        stacked_imgs = np.stack(imgs_list, axis=2)
        min = np.amin(stacked_imgs, axis=2)
        max = np.amax(stacked_imgs, axis=2)

        # Direct/Global(ambient) light component estimates at each image pixel according to
        # "Simple, accurate, Robust projector-camera calibration" by Moreno and Taubin

        # direct <- 0 of ret
        # ambient <- 1 of ret

        ret[:,:,0] = (max - min) / (1-b)
        ret[:,:,1] = 2 * (min - b*max) / (1-b*b)


        return ret











d =  Decoder(ROOT_DIR)
d.decode()