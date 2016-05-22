
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


def set_labels(config, plot, indices):
    if config is None:
        return
    plot.set_xlabel(config.axes[indices[0]].label)
    plot.set_ylabel(config.axes[indices[1]].label)
    plot.set_zlabel(config.axes[indices[2]].label)
    

def plot_nonlinear_confidence_region_3D_projections_combinatorial(config, region):
    """
    Shows at the end
    config  TODOC
    data    numpy.array
    """
    # HACK
    data = region[0:1000]
    fig = pp.figure("3D NCR projections")
    
    sp = fig.add_subplot(2, 2, 1, projection='3d')
    indices = [0,1,2]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    set_labels(config, sp, indices)
    
    sp = fig.add_subplot(2, 2, 2, projection='3d')
    indices = [0,1,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    set_labels(config, sp, indices)
    
    sp = fig.add_subplot(2, 2, 3, projection='3d')
    indices = [0,2,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    set_labels(config, sp, indices)
    
    sp = fig.add_subplot(2, 2, 4, projection='3d')
    indices = [1,2,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    set_labels(config, sp, indices)
    
    pp.show()
    
    
def plot_3d_combinatorial(data):
    '''
    Legacy. Use:
    plot_nonlinear_confidence_region_3D_projections_combinatorial
    data    numpy.array
    '''
    plot_nonlinear_confidence_region_3D_projections_combinatorial(None, data)
