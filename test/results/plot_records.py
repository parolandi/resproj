
import unittest
import results.plot_records as testme

import common.environment as coen

class TestPlotRecords(unittest.TestCase):

    def test_read_trajectories_from_files(self):
        [time, vals] = testme.read_trajectories_from_files( \
            coen.get_results_location()+"test_read_trajectories_from_files.csv")
        self.assertAlmostEqual(time[1], 2.0, places=10)
        self.assertAlmostEqual(vals[0,0], 0.1, places=10)
    
    # TODO
    # missing
    # test_plot_tiled_calibration_and_validation_trajectories_at_record
    
if __name__ == "__main__":
    unittest.main()