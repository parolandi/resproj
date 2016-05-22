
import unittest
import results.plot_3d as testme

import numpy as np

import common.environment as coen
import results.plot_data as replda


class TestPlot3d(unittest.TestCase):

    def get_plot_config(self):
        config = replda.TiledPlotFormattingData(4)
        config.set_axes_data( \
            replda.PlotAxisFormattingData().set_min_max_label(0,0,"p1"), 0). \
        set_axes_data(
            replda.PlotAxisFormattingData().set_min_max_label(0,0,"p2"), 1). \
        set_axes_data(
            replda.PlotAxisFormattingData().set_min_max_label(0,0,"p3"), 2). \
        set_axes_data(
            replda.PlotAxisFormattingData().set_min_max_label(0,0,"p4"), 3)
        return config
    

    def dn_test_plot_3d_from_file(self):
        region = np.loadtxt(coen.get_test_mock_location() + "/multiplepoints.txt", delimiter=',')
        testme.plot_3d(region, [1,2,3])
        self.assertTrue(True)

    
    def dn_test_plot_3d_combinatorial_from_file(self):
        region = np.loadtxt(coen.get_test_mock_location() + "/multiplepoints.txt", delimiter=',')
        testme.plot_3d_combinatorial(region)
        self.assertTrue(True)


    def test_plot_nonlinear_confidence_region_3D_projections_combinatorial(self):
        config = self.get_plot_config()
        region = np.loadtxt(coen.get_test_mock_location() + "/multiplepoints.txt", delimiter=',')
        testme.plot_nonlinear_confidence_region_3D_projections_combinatorial(config, region)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()