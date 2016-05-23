
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as pp

import logging

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
    

def set_ticks(plot, config, indices):
    if config is None:
        return
    plot.set_xticks(config.axes[indices[0]].get_major_ticks())
    plot.set_yticks(config.axes[indices[1]].get_major_ticks())
    plot.set_zticks(config.axes[indices[2]].get_major_ticks())
    

def plot_nonlinear_confidence_region_3D_projections_combinatorial(config, region):
    """
    Shows at the end
    config  TODOC
    data    numpy.array
    """
    # HACK
    if len(region) >= 1000:
        msg = "plotting; 3D projections: was hoping to plot" + str(len(region)) + " points; now only plotting 1000"
    else:
        msg = "plotting; 3D projections: was hoping to plot 1000 points; now only plotting " + str(len(region))
    logging.info(msg)
    print(msg)  
    data = region[0:1000]
    fig = pp.figure("3D NCR projections", figsize=(8,8))
    
    sp = fig.add_subplot(2, 2, 1, projection='3d')
    indices = [0,1,2]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    set_labels(config, sp, indices)
    set_ticks(sp, config, indices)
    
    sp = fig.add_subplot(2, 2, 2, projection='3d')
    indices = [0,1,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    set_labels(config, sp, indices)
    set_ticks(sp, config, indices)
    
    sp = fig.add_subplot(2, 2, 3, projection='3d')
    indices = [0,2,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    set_labels(config, sp, indices)
    set_ticks(sp, config, indices)
    
    sp = fig.add_subplot(2, 2, 4, projection='3d')
    indices = [1,2,3]
    sp.scatter(np.transpose(data)[indices[0]], \
                    np.transpose(data)[indices[1]], \
                    np.transpose(data)[indices[2]])
    set_labels(config, sp, indices)
    set_ticks(sp, config, indices)
    
    pp.subplots_adjust( \
        left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.10, hspace=0.10)
    pp.show()
    
    
def plot_3d_combinatorial(data):
    '''
    Legacy. Use:
    plot_nonlinear_confidence_region_3D_projections_combinatorial
    data    numpy.array
    '''
    plot_nonlinear_confidence_region_3D_projections_combinatorial(None, data)
