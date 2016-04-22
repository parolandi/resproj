
import common.io as coio
import results.plot_combinatorial as replco
import results.plot_3d as repl3d
import numpy as np
import pandas as pd

import scipy.spatial as scsp
import matplotlib.pyplot as pp

def read_points_and_get_interval_bounds():
    pathfile = "/Users/mamuts/code/Desktop/ncr-param-vals.csv"
    raw = coio.read_from_csv(pathfile)
    data = pd.DataFrame(raw)
    bounds = []
    bounds.append(data.min())
    bounds.append(data.max())
    print(bounds)
    

def read_ncr_points_from_csv_and_plot_ND():
    pathfile = "/Users/mamuts/code/Desktop/ncr-param-vals.csv"
    raw = coio.read_from_csv(pathfile)
    # remember to transpose
    replco.plot_combinatorial_region_projections(np.transpose(raw))
    repl3d.plot_3d_combinatorial(raw[0:1000])

# -----------------------------------------------------------------------------
# Fluxing
def read_ncr_points_from_csv_and_plot_2D_and_hull():
    pathfile = "/Users/mamuts/code/Desktop/ncr-param-vals.csv"
    raw = coio.read_from_csv(pathfile)
    # remember to transpose
    pnts = np.transpose(np.transpose(raw)[0:2]) # 0-1
    #pnts = np.transpose(np.transpose(raw)[1:3]) # 1-2
    pnts = np.transpose(np.transpose(raw)[2:])
    # 0-3, 0-2, 1-3, #2-3
    hull = scsp.ConvexHull(pnts)
    tri = scsp.Delaunay(pnts)
    pp.plot(np.transpose(pnts)[0], np.transpose(pnts)[1], 'o')
    for simplex in hull.simplices:
        pp.plot(pnts[simplex, 0], pnts[simplex, 1], 'k-')
    scsp.delaunay_plot_2d(tri)
    pp.show()
    #replco.plot_combinatorial_region_projections(np.transpose(raw))
    
    
# -----------------------------------------------------------------------------
# Legacy
def read_ncr_points_from_csv_and_plot():
    pathfile = "/Users/mamuts/code/Desktop/pnts.txt"
    offset = 0
    nps = 1631
    # this gets rid of the header and footer, but intermediate sections need to be edited manually
    raw = coio.read_from_csv(pathfile)
    # get points only (not objective function) and remove dataframe index (point count)
    pnts = np.transpose(np.transpose(raw[offset:nps])[1:])
    # remember to transpose
    replco.plot_combinatorial_region_projections(np.transpose(pnts))
    repl3d.plot_3d_combinatorial(pnts[0:1000])
    data = pd.DataFrame(pnts)
    bounds = []
    bounds.append(data.min())
    bounds.append(data.max())
    print(bounds)
    pnts1 = pnts
    '''
    offset = 215
    nps = 122+offset
    # this gets rid of the header and footer, but intermediate sections need to be edited manually
    raw = coio.read_from_csv(pathfile)
    # get points only (not objective function) and remove dataframe index (point count)
    pnts = np.transpose(np.transpose(raw[offset:nps])[1:])
    # remember to transpose
    replco.plot_combinatorial_region_projections(np.transpose(pnts))
    data = pd.DataFrame(pnts)
    bounds = []
    bounds.append(data.min())
    bounds.append(data.max())
    print(bounds)
    pnts2 = pnts
    #'''
    #allpnts = np.concatenate((pnts1, pnts2))
    #replco.plot_combinatorial_region_projections(np.transpose(allpnts))
    #repl3d.plot_3d_combinatorial(allpnts[0:1000])
    #repl3d.plot_3d(allpnts[0:1000], [0,1,2])
    
    
if __name__ == "__main__":
    #read_ncr_points_from_csv_and_plot()
    #read_points_and_get_interval_bounds()
    read_ncr_points_from_csv_and_plot_ND()
    #read_ncr_points_from_csv_and_plot_2D_and_hull()