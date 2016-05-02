
import unittest
import results.plot_strips as testme

import results.plot_data as repd

class TestPlotStrips(unittest.TestCase):


    def test_multi_basic(self):
        data = repd.TimeCourseData()
        data.independent = [0,1,2,3]
        data.measurements = [[0,1,2,3], [10,11,12,13]]
        data.predictions = [[0.1,1.1,2.1,3.1], [10.1,11.1,12.1,13.1]]
        data.errors = None
        
        config = repd.MultiPlotFormattingData(2)
        config.layout.no_cols = 1
        config.layout.no_rows = config.count
        config.layout.indices = [0,1]
        
        config.multi_plots[0].y_axis.label = "y0"
        config.multi_plots[0].x_axis.label = "x"
        config.multi_plots[1].y_axis.label = "y1"
        config.multi_plots[0].x_axis.label = "x"
        
        testme.plot_measurements_with_trajectories_with_errors( \
            data, config)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()