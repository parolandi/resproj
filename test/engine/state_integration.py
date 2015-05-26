
import unittest
import engine.state_integration as testme
import test.mock.mock as testmetoo

import numpy

import models.model_data as momoda


class TestStateIntegration(unittest.TestCase):


    def test_compute_timecourse_trajectories(self):
        model, problem = testmetoo.do_setup(numpy.arange(10))
        actual = testme.compute_timecourse_trajectories(model, problem)
        print(actual)
        problem["output_filters"] = dict(momoda.output_filters)
        problem["output_filters"]["measurement_splices"] = [slice(0,5,1)]
        actual = testme.compute_timecourse_trajectories(model, problem)
        print(actual)
        self.assertTrue(False)


    def test_compute_calibration_and_validation_timecourse_trajectories(self):
        model, problem = testmetoo.do_setup(numpy.arange(10))
        actual = testme.compute_calibration_and_validation_timecourse_trajectories(model, problem)
        

if __name__ == "__main__":
    unittest.main()