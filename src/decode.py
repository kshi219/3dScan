from skimage import color
from skimage import io
from skimage import img_as_ubyte
from glob import glob
import numpy as np
from matplotlib import pyplot as plt
import code_convert



ROOT_DIR = '/home/kevin/Desktop/learningResources/3dscan/cartman/'
DIRECT_EST_PARAM = 0.3
THRESH_PARAM = 5
PROJ = [640, 720]


class Decoder():

    def __init__(self, image_dir=ROOT_DIR):
        print DIRECT_EST_PARAM
        self.views = glob(image_dir + '*/')
        # pattern images organized in order of least to most dense and vertical -> horizontal patterns
        self.images = sorted(glob(self.views[0] + '*.png'))
        self.size = io.imread(self.images[0]).shape[0:2]
        self.decoded_indices = np.zeros(self.size + (2,), dtype=int)
        self.minmax_img = np.zeros(self.size + (2,), dtype=int)
        # assuming binary gray code pattern
        self.bits = (len(self.images)/2 - 1)/2
        self.nan_thresh = 1 << self.bits + 1
        self.patterns = self.bits * 2
        self.curr_bit = self.bits - 1
        self.offset = [int(((1 << self.bits) - PROJ[0])/2),int(((1 << self.bits) - PROJ[1])/2)]
        self.proj = PROJ


    def decode(self):

        # we estimate the direct and ambient sources of light using the second to last most dense pattern images
        img1 = []
        img2 = []
        offset = self.patterns
        start = len(self.images) - offset - 6 - 2
        for i in xrange(0,4):
            print self.images[start + i + 2]
            print self.images[start + i + offset]
            img1.append(self.images[start + i])
            img2.append(self.images[start + i + offset])
        set_imgs =  img1 + img2
        direct_comps_img = self.direct_est(set_imgs, DIRECT_EST_PARAM)
        dimg_size = direct_comps_img.shape[0:2]

        # inspect each pair of images and perform pattern decoding

        # first two images in set are not pattern images
        images = self.images[2:]
        # the first (self.patterns) images are verticle patterns and the rest are horizontal
        channel = 0
        for i in xrange(0,40):
            if (i % 2) != 0:
                continue
            print "progress: " + str(i)
            if i  == self.patterns:
                # vertical
                channel += 1
                self.curr_bit = self.bits - 1

            img1 = img_as_ubyte(io.imread(images[i], as_grey=True))
            img2 = img_as_ubyte(io.imread(images[i+1], as_grey=True))

            if not (img1.shape == self.decoded_indices.shape[0:2]):
                print "pattern image shapes not as expected"
            if not (img1.shape == img2.shape):
                print "corresponding pattern image shapes not identical"
            if not (img1.shape == dimg_size):
                print "direct light images shape and pattern image shapes not identical"

            # min_max image determination
            if i == 0:
                stacked_imgs = np.stack([img1, img2], axis=2)
                self.minmax_img[:,:,0] = np.amin(stacked_imgs, axis=2)
                self.minmax_img[:,:,1] = np.amax(stacked_imgs, axis=2)
            else:
                stacked_imgs = np.stack([img1, img2, self.minmax_img[:, :, 0], self.minmax_img[:, :, 1]], axis=2)
                self.minmax_img[:, :, 0] = np.amin(stacked_imgs, axis=2)
                self.minmax_img[:, :, 1] = np.amax(stacked_imgs, axis=2)

            pattern_stack = np.stack([img1, img2, direct_comps_img[:, :, 0], direct_comps_img[:, :, 1]], axis=2)
            out = np.apply_along_axis(self.robust_bit_est, 2, pattern_stack)
            self.decoded_indices[:, :, channel] |= out

            self.curr_bit -= 1
        #
        # temp = self.decoded_indices[:, :, 1] + self.decoded_indices[:, :, 0]
        #
        # temp[temp>=self.nan_thresh] = 0
        # temp[temp>0] = 1
        #
        # io.imshow(temp)
        # plt.show()

        self.decoded_indices = code_convert.convert_pattern(self.decoded_indices, PROJ, self.offset, self.nan_thresh)

        # temp = self.decoded_indices
        #
        # io.imshow(temp[:,:,0])
        # plt.show()
        #
        # io.imshow(temp[:,:,1])
        # plt.show()



    def robust_bit_est(self, a):
        v1 = a[0]
        v2 = a[1]
        Ld = a[2]
        Lg = a[3]
        m = THRESH_PARAM
        if Ld < m:
            return self.nan_thresh
        if Ld > Lg:
            if v1 > v2:
                return 1 << self.curr_bit
            else:
                return 0
        # if v1 > v2:
        #         return 1 << self.curr_bit
        # else:
        #         return 0
        # if v1 <= Ld and v2 >= Lg:
        #     return 0
        # if v1 >= Lg and v2 <= Ld:
        #     return 1 << self.curr_bit

        return self.nan_thresh


    def direct_est(self, imgs, b):
        ret = np.empty(self.minmax_img.shape, dtype=int)
        imgs_list = []
        for i in imgs:
            img = img_as_ubyte(io.imread(i, as_grey=True)).astype(np.float64)
            imgs_list.append(img)
        stacked_imgs = np.stack(imgs_list, axis=2)
        min = np.amin(stacked_imgs, axis=2)
        max = np.amax(stacked_imgs, axis=2)

        # Direct/Global(ambient) light component estimates at each image pixel according to
        # "Simple, accurate, Robust projector-camera calibration" by Moreno and Taubin

        # direct <- 0 of ret
        # ambient <- 1 of ret

        ret[:,:,0] = np.uint8((max - min) / (1.0-b))
        ret[:,:,1] = np.uint8(2.0 * (min - b*max) / (1.0-b*1.0*b))

        return ret



# d =  Decoder(ROOT_DIR)
# d.decode()