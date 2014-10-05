
import unittest
import numpy

import common.utilities
import solvers.initial_value
import models.model_data


# states, time, parameters, inputs
def linear_mock(x, t, p, u):
    return p[0] * u[0]


class TestInitialValueSolvers(unittest.TestCase):

    
    def do_setup(self):
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = 0.0
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        return model_instance, problem_instance


    # returns 10 points from 0.0:0.9 inclusive
    def do_setup_include_initial(self):
        model_instance, problem_instance = self.do_setup()
        problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        return model_instance, problem_instance

    
    # returns 10 points from 0.1:1.0 inclusive
    def do_setup_exclude_initial(self):
        model_instance, problem_instance = self.do_setup()
        problem_instance["time"] = numpy.linspace(0.1, 1.0, 10, endpoint=True)
        return model_instance, problem_instance

    
    def test_solve_lsoda_st_include_initial(self):
        model_instance, problem_instance = self.do_setup_include_initial()
        
        result, _ = solvers.initial_value.solve_lsoda_st(linear_mock, model_instance, problem_instance)
        actual = common.utilities.sliceit_assnapshot(result)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]

      
    def test_compute_trajectory_st_include_initial(self):
        model_instance, problem_instance = self.do_setup_include_initial()
                
        actual = solvers.initial_value.compute_trajectory_st(linear_mock, model_instance, problem_instance)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]


    # test that method does NOT handle open initial
    def test_solve_lsoda_st_does_not_exclude_initial(self):
        model_instance, problem_instance = self.do_setup_include_initial()
        problem_instance["initial"] = "exclude"
        
        result, _ = solvers.initial_value.solve_lsoda_st(linear_mock, model_instance, problem_instance)
        actual = common.utilities.sliceit_assnapshot(result)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]

      
    # test that method does handle open initial
    def test_compute_timecourse_trajectories_exclude_initial(self):
        model_instance, problem_instance = self.do_setup_exclude_initial()
        problem_instance["initial"] = "exclude"
                
        actual = solvers.initial_value.compute_timecourse_trajectories(linear_mock, model_instance, problem_instance)
        expected = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]


if __name__ == "__main__":
    unittest.main()
