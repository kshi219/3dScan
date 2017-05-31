import numpy as np
from calibration import Calib
from decode import Decoder
from collections import defaultdict


THRESH = 25
MAX_DIST = 100.0

class reconstruct():
    def __init__(self):
        self.decoded = Decoder()
        self.decoded.decode()
        self.calib = Calib()
        self.minmax = self.decoded.minmax_img
        self.pattern = self.decoded.decoded_indices
        self.proj = (self.decoded.proj[1], self.decoded.proj[0])
        self.out_cols = self.decoded.proj[1]
        self.out_rows = self.decoded.proj[0]
        self.pointcloud = np.zeros((self.out_rows, self.out_cols, 3))
        self.cam_points = defaultdict(list)
        self.proj_points = {}
        self.threshold = THRESH
        self.max_dist = MAX_DIST

    def reconstruct(self):

        def pattern_invalid(thresh, pattern, minmax):
            check = pattern[0] < 0                  \
                    or pattern[0] >= self.proj[0]   \
                    or pattern[1] < 0               \
                    or pattern[1] >= self.proj[1]   \
                    or minmax[1] - minmax[0] < thresh
            return check

        # create 1-to-many correspondnence between projector coordinates
        # and camera coordinates
        pattern = self.pattern
        minmax = self.minmax
        for i in np.ndindex(pattern.shape[:2]):

            if pattern_invalid(self.threshold, pattern[i], minmax[i]):
                continue
            proj_point = pattern[i]
            index = proj_point[1]*self.out_cols + proj_point[0]
            self.proj_points[index] = proj_point
            self.cam_points[index].append(i)

        # find average of the many camera coordinates
        # for each projector coordinate
        for key in self.proj_points.keys():

            proj_point = self.proj_points[key]
            cam_points = self.cam_points[key]
            count = len(cam_points)
            if count == 0: continue
            x = 0
            y = 0
            for point in cam_points:
                y += point[0]
                x += point[1]
            y /= count
            x /= count
            cam = (x,y)
            proj = proj_point

            p, dist = self.triangulate_stereo(cam,proj)

            if dist < self.max_dist:
                self.pointcloud[(proj[1], proj[0])] = np.asarray(p).flatten()

        np.save('cloud.npy', self.pointcloud)
        print "done"


    def triangulate_stereo(self, p1, p2):
        K1 = self.calib.cam_K
        K2 = self.calib.proj_K
        Rt = np.mat(self.calib.Rt)
        T = np.mat(self.calib.T)
        p_1 = np.array(p1, dtype=float)
        p_2 = np.array(p2, dtype=float)
        #TODO apply radial and tangential undistortion
        u1 = np.array(((p_1[0] - K1[0, 2]) / K1[0, 0], (p_1[1] - K1[1, 2]) / K1[1, 1], 1.0), dtype=float)
        u2 = np.array(((p_2[0] - K2[0, 2]) / K2[0, 0], (p_2[1] - K2[1, 2]) / K2[1, 1], 1.0), dtype=float)
        u1 = np.mat(u1).reshape(3, 1)
        u2 = np.mat(u2).reshape(3, 1)

        v1 = u1
        v2 = Rt * (u2 - T)

        w1 = v1
        w2 = Rt * u2


        p, dist = self.appox_ray_x(v1,w1,v2,w2)

        return p, dist


    def appox_ray_x(self, v1, q1, v2, q2):

        v1tv1 = float(v1.transpose() * v1)
        v1tv2 = float(v1.transpose() * v2)
        v2tv1 = float(v2.transpose() * v1)
        v2tv2 = float(v2.transpose() * v2)
        detV = v1tv1*v2tv2 - v1tv2*v2tv2

        q2_q1 = q2 - q1
        Q1 = float(v1.transpose() * q2_q1)
        Q2 = -1.0 * float(v2.transpose() * q2_q1)

        lam1 = (v2tv2 * Q1 + v1tv2 * Q2) / detV
        lam2 = (v2tv1 * Q1 + v1tv1 * Q2) / detV

        p1 = lam1*v1 + q1
        p2 = lam2*v2 + q2

        p3d = 0.5*(p1+p2)

        dist = np.linalg.norm(p2-p1)


        return p3d, dist




if __name__ == '__main__':
    recon = reconstruct()
    recon.reconstruct()





