
import matplotlib.pyplot as pp
from matplotlib.patches import Ellipse
import numpy


def plot_combinatorial_region_projections(region):
    """
    Plots the combination of 2D projections of the nonlinear confidence region
    region    points
    """
    no_grid = region.shape[0]
    fig = pp.figure("NCR projections")
    for cols in range(no_grid):
        for rows in range(no_grid):
            if cols == rows:
                pass
            else:
                plot_no = no_grid*rows+cols+1
                sp = fig.add_subplot(no_grid, no_grid, plot_no)
                sp.plot(region[cols], region[rows], 'o')
    pp.show()


def plot_combinatorial_ellipsoid_projections(center, ell):
    """
    Plots the combination of 2D projections (ellipsoids) of the quadratic confidence region
    center    center of the ellipsoid
    ell       ellipsoid, list of list 
    """
    ellipsoid = numpy.asmatrix(ell)
    # TODO: preconditions

    no_grid = ellipsoid.shape[0]
    fig = pp.figure("LCR projections")
    for cols in range(no_grid):
        for rows in range(no_grid):
            if rows == cols:
                pass
            else:
                subell = ellipsoid[numpy.ix_([rows,cols],[rows,cols])]
                eigenvals, eigenvecs = numpy.linalg.eig(subell)
                # sign eigenvals
                lambdaa = numpy.sqrt(eigenvals)

                plot_no = no_grid*cols+rows+1
                ax = fig.add_subplot(no_grid, no_grid, plot_no)
                ell = Ellipse(xy     = [center[rows],center[cols]], \
                              width  = lambdaa[0]*2, \
                              height = lambdaa[1]*2, \
                              angle  = numpy.rad2deg(numpy.arccos(eigenvecs[0,0])))
                # TODO
                # handle_plot_data(fig, plot_data)
                ax.add_artist(ell)
                ell.set_clip_box(ax.bbox)
                
                sf = 1.0
                height = numpy.sqrt(subell[0,0]) * sf
                width = numpy.sqrt(subell[1,1]) * sf
                ax.set_xlim(center[rows]-height, center[rows]+height)
                ax.set_ylim(center[cols]-width, center[cols]+width)
                
                ell.set_facecolor('none')
    pp.show()
