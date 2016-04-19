
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as pp


def plot_3d(data, indices):
    fig = pp.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    pp.show()
   

def plot_3d_combinatorial(data):
    '''
    data    numpy.array
    '''
    #no_grid = 4
    fig = pp.figure("NCR projections")
    sp = fig.add_subplot(2, 2, 1, projection='3d')
    indices = [0,1,2]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    sp = fig.add_subplot(2, 2, 2, projection='3d')
    indices = [0,1,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    sp = fig.add_subplot(2, 2, 3, projection='3d')
    indices = [0,2,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    sp = fig.add_subplot(2, 2, 4, projection='3d')
    indices = [1,2,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    pp.show()
