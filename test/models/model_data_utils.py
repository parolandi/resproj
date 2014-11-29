
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


if __name__ == "__main__":
    unittest.main()
