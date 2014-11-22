
import unittest
import models.model_data_utils as mmdu

import numpy

import models.model_data as mmd


class Test(unittest.TestCase):

    # TODO: check more than dimensions only
    def test_get_sensitivity_trajectories(self):
        problem = dict(mmd.problem_structure)
        problem["parameter_indices"] = [1,2] 
        problem["output_indices"] = [1,3]
        dim_states = 4
        dim_params = 3
        state_and_sens_trajectories = []
        for ii in range(dim_states + dim_params * dim_states):
            state_and_sens_trajectories.append(numpy.linspace(0+ii, 1+ii, 5))
        sens_trajectories = mmdu.get_sensitivity_trajectories(dim_states, problem, state_and_sens_trajectories)
        actual = len(sens_trajectories)
        self.assertEquals(actual, 4)


if __name__ == "__main__":
    unittest.main()
