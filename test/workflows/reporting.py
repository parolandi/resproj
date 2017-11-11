
import unittest
import workflows.reporting_unlegacy as testme
import test.mock.mock as testmetoo

import numpy
import logging

import common.diagnostics as codi

    
class TestReporting(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestReporting, self).__init__(*args, **kwargs)
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info(codi.get_date_and_time())


    def test_plot_tiled_calibration_validation_and_residual_trajectories_at_point(self):
        point = {}
        point["decision_variables"] = numpy.array([1.0, 2.0])
        testme.plot_tiled_calibration_and_validation_trajectories_at_point(testmetoo.do_experiment(), point)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()