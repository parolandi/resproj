
import common.io as coio
import results.plot_combinatorial as replco
import results.plot_3d as repl3d
import numpy as np
import pandas as pd

def read_ncr_points_from_csv_and_plot():
    pathfile = "C:/Users/mamuts/Desktop/res.csv"
    offset = 0
    nps = 104
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
    pnts1 = pnts
    #'''
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
    allpnts = np.concatenate((pnts1, pnts2))
    replco.plot_combinatorial_region_projections(np.transpose(allpnts))
    repl3d.plot_3d_combinatorial(allpnts[0:1000])
    #repl3d.plot_3d(allpnts[0:1000], [0,1,2])
    
    
if __name__ == "__main__":
    read_ncr_points_from_csv_and_plot()