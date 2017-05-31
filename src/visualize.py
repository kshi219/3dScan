

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 20
w.show()
w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')


cloud = np.load('cloud.npy')
x = cloud[:,:,0].flatten()
y = cloud[:,:,1].flatten()
z = cloud[:,:,2].flatten()

x = x*100 - 10
y = -1*(y*100) + 10
z = -1*(z*1000 -970)

N = max(x.shape)
pos = np.empty((N,3))
pos[:, 0] = x
pos[:, 1] = z
pos[:, 2] = y



sp1 = gl.GLScatterPlotItem(pos=pos, size=0.03, color=(0.0, 0.0, 1.0, 0.5), pxMode=False)
sp1.scale(0.18,0.18,0.18)
w.addItem(sp1)




def update():
    sp1.rotate(1.5,0,0,1)

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()