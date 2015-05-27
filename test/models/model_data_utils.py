
import unittest
import models.model_data_utils as testme

import numpy

import models.model_data as mmd


class TestModelDataUtils(unittest.TestCase):

    def test_get_sensitivity_trajectories(self):
        problem = dict(mmd.problem_structure)
        problem["parameters"] = [0,1,2]
        problem["parameter_indices"] = [0,1,2] 
        problem["output_indices"] = [1,3]
        dim_states = 4
        dim_params = 3
        state_and_sens_trajectories = []
        for ii in range(dim_states + dim_params * dim_states):
            state_and_sens_trajectories.append(numpy.linspace(0+ii, 1+ii, 5))
        sens_trajectories = testme.get_sensitivity_trajectories(dim_states, problem, state_and_sens_trajectories)
        expected_o1p0 = numpy.linspace(0+7, 1+7, 5)
        expected_o1p1 = numpy.linspace(0+8, 1+8, 5)
        expected_o1p2 = numpy.linspace(0+9, 1+9, 5)
        expected_o3p0 = numpy.linspace(0+13, 1+13, 5)
        expected_o3p1 = numpy.linspace(0+14, 1+14, 5)
        expected_o3p2 = numpy.linspace(0+15, 1+15, 5)
        [self.assertEquals(act, exp) for act, exp in zip(sens_trajectories[0], expected_o1p0)]
        [self.assertEquals(act, exp) for act, exp in zip(sens_trajectories[1], expected_o1p1)]
        [self.assertEquals(act, exp) for act, exp in zip(sens_trajectories[2], expected_o1p2)]
        [self.assertEquals(act, exp) for act, exp in zip(sens_trajectories[3], expected_o3p0)]
        [self.assertEquals(act, exp) for act, exp in zip(sens_trajectories[4], expected_o3p1)]
        [self.assertEquals(act, exp) for act, exp in zip(sens_trajectories[5], expected_o3p2)]
        self.assertEquals(len(sens_trajectories), 6)


    def test_get_observable_trajectories(self):
        problem = dict(mmd.problem_structure)
        problem["output_indices"] = [1,3]
        dim_states = 4
        state_trajectories = []
        for ii in range(dim_states):
            state_trajectories.append(numpy.linspace(0+ii, 1+ii, 5))
        obs_trajectories = testme.get_observable_trajectories(problem, state_trajectories)
        expected_o1 = numpy.linspace(0+1, 1+1, 5)
        expected_o3 = numpy.linspace(0+3, 1+3, 5)
        [self.assertEquals(act, exp) for act, exp in zip(obs_trajectories[0], expected_o1)]
        [self.assertEquals(act, exp) for act, exp in zip(obs_trajectories[1], expected_o3)]
        self.assertEquals(len(obs_trajectories), 2)


    def test_get_observable_calibration_and_validation_trajectories(self):
        problem = dict(mmd.problem_structure)
        problem["output_indices"] = [1,3]
        dim_states = 4
        
        calib_trajectories = []
        valid_trajectories = []
        for ii in range(dim_states):
            calib_trajectories.append(numpy.linspace(0+ii, 1+ii, 5))
            valid_trajectories.append(numpy.linspace(10+ii, 11+ii, 5))
        calib_time = numpy.linspace(0,4,5)
        valid_time = numpy.linspace(10,14,5)
        calib_valid_trajectories = dict(mmd.calib_valid_experimental_dataset)
        calib_valid_trajectories["calib"]["time"] = calib_time
        calib_valid_trajectories["calib"]["observables"] = numpy.asarray(calib_trajectories)
        calib_valid_trajectories["valid"]["time"] = valid_time
        calib_valid_trajectories["valid"]["observables"] = numpy.asarray(valid_trajectories)
        
        obs_trajectories = testme.get_observable_calibration_and_validation_trajectories( \
            calib_valid_trajectories, problem)
        
        expected_calib_t = numpy.linspace(0, 4, 5)
        expected_calib_o1 = numpy.linspace(0+1, 1+1, 5)
        expected_calib_o3 = numpy.linspace(0+3, 1+3, 5)
        expected_valid_t = numpy.linspace(10, 14, 5)
        expected_valid_o1 = numpy.linspace(10+1, 11+1, 5)
        expected_valid_o3 = numpy.linspace(10+3, 11+3, 5)
        
        [self.assertEquals(act, exp) for act, exp in zip(obs_trajectories["calib"]["time"], expected_calib_t)]
        [self.assertEquals(act, exp) for act, exp in zip(obs_trajectories["calib"]["observables"][0], expected_calib_o1)]
        [self.assertEquals(act, exp) for act, exp in zip(obs_trajectories["calib"]["observables"][1], expected_calib_o3)]
        [self.assertEquals(act, exp) for act, exp in zip(obs_trajectories["valid"]["time"], expected_valid_t)]
        [self.assertEquals(act, exp) for act, exp in zip(obs_trajectories["valid"]["observables"][0], expected_valid_o1)]
        [self.assertEquals(act, exp) for act, exp in zip(obs_trajectories["valid"]["observables"][1], expected_valid_o3)]
        
    
    
    def test_get_measurements_for_all_experiments(self):
        experiment = {}
        experiment["output_measurements"] = [0, 1, 2, 3, 4]
        problem = {}
        problem["experiments"] = [experiment, experiment]
        actual = testme.get_measurement_template_for_all_experiments(problem)
        self.assertEquals(len(actual), 10)

        experiment["output_measurements"] = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
        problem = {}
        problem["experiments"] = [experiment, experiment]
        actual = testme.get_measurement_template_for_all_experiments(problem)
        self.assertEquals(len(actual), 20)


if __name__ == "__main__":
    unittest.main()
