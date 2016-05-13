
import matplotlib.pyplot as pp
from matplotlib.patches import Ellipse
import numpy


def regularise_ellipsoid(subell, scale):
    subell = numpy.asmatrix( \
        [[subell[0,0]/scale[0]**2, \
          subell[0,1]/scale[0]/scale[1]], \
         [subell[1,0]/scale[0]/scale[1], \
          subell[1,1]/scale[1]**2]])
    return subell


def plot_qudratic_confidence_region_2D_ellipsoid( \
    config, center, ellipsoid, no_grid, rows, cols, fig):
    subell = ellipsoid[numpy.ix_([rows,cols],[rows,cols])]
    regularise = True
    if regularise:
        scale = [1E7, 0.1, 10, 1E-5]
        subell = regularise_ellipsoid(subell, [scale[rows-1],scale[cols-1]])
    eigenvals, eigenvecs = numpy.linalg.eig(subell)
    # sign eigenvals
    lambdaa = numpy.sqrt(eigenvals)

    plot_no = no_grid*cols+rows+1
    ax = fig.add_subplot(no_grid, no_grid, plot_no)
    ell = Ellipse(xy     = [center[rows],center[cols]], \
                  width  = lambdaa[0]*2, \
                  height = lambdaa[1]*2, \
                  angle  = numpy.rad2deg(numpy.arccos(eigenvecs[0,0])))
    ax.add_artist(ell)
    ell.set_clip_box(ax.bbox)
    
    sf = 1.0
    height = numpy.sqrt(subell[0,0]) * sf
    width = numpy.sqrt(subell[1,1]) * sf
    ax.set_xlim(center[rows]-height, center[rows]+height)
    ax.set_ylim(center[cols]-width, center[cols]+width)
    squared = True
    if squared:
        x0,x1 = ax.get_xlim()
        y0,y1 = ax.get_ylim()
        ax.set_aspect(abs(x1-x0)/abs(y1-y0))
    ell.set_facecolor('none')
    ax.set_xlabel(config.axes[rows].label)
    ax.set_ylabel(config.axes[cols].label)

    
# WIP: scale center as well, mark center of ellipsoid, add value
def plot_qudratic_confidence_region_2D_projections_combinatorial(config, center, ellipse):
    """
    Plots the combination of 2D projections (ellipsoids) of the quadratic confidence region
    center    center of the ellipsoid
    ellipse   ellipsoid, list of list 
    """
    # TODO: preconditions
    ellipsoid = numpy.asmatrix(ellipse)
    no_grid = ellipsoid.shape[0]
    fig = pp.figure("LCR projections")
    for cols in range(no_grid):
        for rows in range(no_grid):
            if rows == cols:
                pass
            else:
                plot_qudratic_confidence_region_2D_ellipsoid( \
                    config, center, ellipsoid, no_grid, rows, cols, fig)
    pp.show()


def plot_nonlinear_confidence_region_2D_scatter( \
    config, region, no_grid, rows, cols, fig):
    plot_no = no_grid*rows+cols+1
    sp = fig.add_subplot(no_grid, no_grid, plot_no)
    sp.plot(region[cols], region[rows], 'o')
    sp.set_xlabel(config.axes[cols].label)
    sp.set_ylabel(config.axes[rows].label)
    

# remember to transpose
def plot_nonlinear_confidence_region_2D_projections_combinatorial(config, realisations):
    """
    Plots the combination of 2D projections of the nonlinear confidence region
    """
    # TODO: preconditions
    region = numpy.transpose(realisations)
    no_grid = region.shape[0]
    fig = pp.figure("NCR projections")
    for cols in range(no_grid):
        for rows in range(no_grid):
            if cols == rows:
                pass
            else:
                plot_nonlinear_confidence_region_2D_scatter( \
                    config, region, no_grid, rows, cols, fig)
    pp.show()
