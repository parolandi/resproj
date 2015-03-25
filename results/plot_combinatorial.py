
import matplotlib.pyplot as pp
from matplotlib.patches import Ellipse
import numpy


def plot_combinatorial_region_projections(region):
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
    ellipsoid = numpy.asmatrix(ell)
    # TODO: preconditions
    # sign eigenvals
    eigenvals, eigenvecs = numpy.linalg.eig(ellipsoid)
    lambdaa = numpy.sqrt(eigenvals)

    no_grid = ellipsoid.shape[0]
    fig = pp.figure("LCR projections")
    for cols in range(no_grid):
        for rows in range(no_grid):
            if rows == cols:
                pass
            else:
                plot_no = no_grid*rows+cols+1
                ax = fig.add_subplot(no_grid, no_grid, plot_no)
                ell = Ellipse(xy=center, width=lambdaa[cols]*2, height=lambdaa[rows]*2, angle=numpy.rad2deg(numpy.arccos(eigenvecs[0,0])))
                #handle_plot_data(fig, plot_data)
                ax.add_artist(ell)
                ell.set_clip_box(ax.bbox)
                
                sf = 1.1
                height = numpy.sqrt(ellipsoid[cols,cols]) * sf
                width = numpy.sqrt(ellipsoid[rows,rows]) * sf
                ax.set_xlim(center[0]-height, center[0]+height)
                ax.set_ylim(center[1]-width, center[1]+width)
                
                ell.set_facecolor('none')
    pp.show()
