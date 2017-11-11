
import unittest
import results.plot_strips as testme

import results.plot_data as repd
from results.plot_data import PlotAxisFormattingData
from results.plot_data import SinglePlotFormattingData
from results.plot_data import MultiPlotLayoutData

class TestPlotStrips(unittest.TestCase):


    def test_multi_basic(self):
        data = repd.TimeCourseData()
        data.independent = [0,1,2,3]
        data.measurements = [[0,1,2,3], [10,11,12,13]]
        data.predictions = [[0.1,1.1,2.1,3.1], [10.1,11.1,12.1,13.1]]
        data.errors = None
        
        count = 2
        config = repd.MultiPlotFormattingData(count).set_layout_data( \
            MultiPlotLayoutData().set_no_cols_no_rows_indices(1, count, [0,1]))
        config.set_formatting_data( \
            SinglePlotFormattingData(). \
                set_x_axis(PlotAxisFormattingData().set_min_max_label(0,0,"x0")). \
                set_y_axis(PlotAxisFormattingData().set_min_max_label(0,0,"y0")), \
                0)
        config.set_formatting_data( \
            SinglePlotFormattingData(). \
                set_x_axis(PlotAxisFormattingData().set_min_max_label(0,0,"x1")). \
                set_y_axis(PlotAxisFormattingData().set_min_max_label(0,0,"y1")), \
                1)
        
        testme.plot_measurements_with_trajectories_with_errors( \
            data, config)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()