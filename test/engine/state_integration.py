
import unittest
import engine.state_integration as testme
import test.mock.mock as testmetoo

import numpy

import models.model_data as momoda


class TestStateIntegration(unittest.TestCase):


    def test_compute_timecourse_trajectories(self):
        config = testmetoo.do_experiment_invariant()
        model = config["model_setup"]()
        problem = config["problem_setup"](None, None)
        assert(problem["output_filters"] is not None)
        problem["output_filters"]["measurement_splices"] = [slice(0,5,1)]
        actual = testme.compute_timecourse_trajectories(model, problem)
        expected = numpy.ones(5)
        [self.assertEquals(act, exp) for act, exp in zip(actual[0], expected)]
        [self.assertEquals(act, exp) for act, exp in zip(actual[1], expected)]


    def test_compute_calibration_and_validation_timecourse_trajectories(self):
        config = testmetoo.do_experiment_invariant()
        model = config["model_setup"]()
        problem = config["problem_setup"](None, None)
        actual = testme.compute_calibration_and_validation_timecourse_trajectories(model, problem)
        expected = momoda.calib_valid_experimental_dataset
        expected["calib"]["time"] = numpy.arange(5)
        expected["calib"]["observables"] = numpy.ones(5)
        expected["valid"]["time"] = numpy.arange(5,10)
        expected["valid"]["observables"] = numpy.ones(5)
        [self.assertEquals(act, exp) for act, exp in zip(actual["calib"]["time"], expected["calib"]["time"])]
        [self.assertEquals(act, exp) for act, exp in zip(actual["calib"]["observables"], expected["calib"]["observables"])]
        [self.assertEquals(act, exp) for act, exp in zip(actual["valid"]["time"], expected["valid"]["time"])]
        [self.assertEquals(act, exp) for act, exp in zip(actual["valid"]["observables"], expected["valid"]["observables"])]
        

if __name__ == "__main__":
    unittest.main()