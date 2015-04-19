
import unittest
import solvers.initial_value

import copy
import numpy

import common.utilities
import models.model_data


# states, time, parameters, inputs
def linear_mock(x, t, p, u):
    return p[0] * u[0]


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    dx_dt = numpy.multiply(p, u)
    return dx_dt


# TODO: test with subset of "dofs"
class TestInitialValueSolvers(unittest.TestCase):

    
    def do_setup(self):
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = [0.0]
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        return model_instance, problem_instance


    def do_setup_2p2s(self):
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = [0.0, 1.0]
        problem_instance["parameters"] = [1.0, 0.5]
        problem_instance["inputs"] = [1.0, 2.0]
        
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = copy.deepcopy(problem_instance["parameters"])
        model_instance["inputs"] = copy.deepcopy(problem_instance["inputs"])
        model_instance["states"] = copy.deepcopy(problem_instance["initial_conditions"])
        model_instance["time"] = 0.0

        return model_instance, problem_instance

    
    def do_setup_2p2s_with_forcing_inputs(self):
        model, problem = self.do_setup_2p2s()
        forcing_inputs = copy.deepcopy(models.model_data.forcing_function_profile)
        forcing_inputs["continuous_time_intervals"] = [0, 0.5, 0.9]
        forcing_inputs["piecewise_constant_inputs"] = [[1, 2], [2, 2]]
        problem["forcing_inputs"] = forcing_inputs
        problem["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        return model, problem

    
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
        # TODO: transform to snapshot
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]

      
    def test_compute_trajectory_st_include_initial(self):
        model_instance, problem_instance = self.do_setup_include_initial()
                
        actual = solvers.initial_value.compute_trajectory_st(linear_mock, model_instance, problem_instance)
        # TODO: transform to snapshot
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
        expected = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[0], actual[0])]


    def test_linear_2p2s_solve_lsoda_st_include_initial(self):
        model_instance, problem_instance = self.do_setup_2p2s()
        problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        
        # avoid false negatives
        model_instance["states"] = numpy.multiply(problem_instance["initial_conditions"], 1.1)
        problem_instance["parameters"] = numpy.multiply(problem_instance["parameters"], 1.1)
        problem_instance["inputs"] = numpy.multiply(problem_instance["inputs"], 1.1)
                
        result, _ = solvers.initial_value.solve_lsoda_st(linear_2p2s_mock, model_instance, problem_instance)
        actual = common.utilities.sliceit_astrajectory(result)
        expected = [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]

        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[0], actual[0])]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[1], actual[1])]


    def test_linear_2p2s_compute_timecourse_trajectories_include_initial(self):
        model_instance, problem_instance = self.do_setup_2p2s()
        problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        
        # avoid false negatives
        model_instance["states"] = numpy.multiply(problem_instance["initial_conditions"], 1.1)
        problem_instance["parameters"] = numpy.multiply(problem_instance["parameters"], 1.1)
        problem_instance["inputs"] = numpy.multiply(problem_instance["inputs"], 1.1)
                
        actual = solvers.initial_value.compute_timecourse_trajectories(linear_2p2s_mock, model_instance, problem_instance)
        expected = [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]
        
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[0], actual[0])]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[1], actual[1])]

    
    # TODO: test that solve_lsoda_st asserts if model is none
    
    
    def test_linear_2p2s_solve_include_initial_model_is_not_none(self):
        model_instance, problem_instance = self.do_setup_2p2s()
        model_instance["model"] = linear_2p2s_mock
        problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        
        # avoid false negatives
        model_instance["states"] = numpy.multiply(problem_instance["initial_conditions"], 1.1)
        problem_instance["parameters"] = numpy.multiply(problem_instance["parameters"], 1.1)
        problem_instance["inputs"] = numpy.multiply(problem_instance["inputs"], 1.1)
                
        _, result, _ = solvers.initial_value.solve(model_instance, problem_instance)
        actual = common.utilities.sliceit_astrajectory(result)
        expected = [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]

        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[0], actual[0])]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[1], actual[1])]


    def test_linear_2p2s_compute_timecourse_trajectories_include_initial_model_is_not_none(self):
        model_instance, problem_instance = self.do_setup_2p2s()
        model_instance["model"] = linear_2p2s_mock
        problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        
        # avoid false negatives
        model_instance["states"] = numpy.multiply(problem_instance["initial_conditions"], 1.1)
        problem_instance["parameters"] = numpy.multiply(problem_instance["parameters"], 1.1)
        problem_instance["inputs"] = numpy.multiply(problem_instance["inputs"], 1.1)
                
        actual = solvers.initial_value.compute_timecourse_trajectories(None, model_instance, problem_instance)
        expected = [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]
        
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[0], actual[0])]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[1], actual[1])]


    def test_evaluate_timecourse_snapshots(self):
        model_instance, problem_instance = self.do_setup_2p2s()
        model_instance["model"] = linear_2p2s_mock
        problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        
        # avoid false negatives
        model_instance["states"] = numpy.multiply(problem_instance["initial_conditions"], 1.1)
        problem_instance["parameters"] = numpy.multiply(problem_instance["parameters"], 1.1)
        problem_instance["inputs"] = numpy.multiply(problem_instance["inputs"], 1.1)
                
        actual = solvers.initial_value.evaluate_timecourse_snapshots(model_instance, problem_instance)
        expected = [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]
        
        self.assertTrue(actual.success)
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[0], actual.snapshots[:,0])]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[1], actual.snapshots[:,1])]
        

    def test_evaluate_timecourse_trajectories(self):
        model_instance, problem_instance = self.do_setup_2p2s()
        model_instance["model"] = linear_2p2s_mock
        problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        
        # avoid false negatives
        model_instance["states"] = numpy.multiply(problem_instance["initial_conditions"], 1.1)
        problem_instance["parameters"] = numpy.multiply(problem_instance["parameters"], 1.1)
        problem_instance["inputs"] = numpy.multiply(problem_instance["inputs"], 1.1)
                
        actual = solvers.initial_value.evaluate_timecourse_trajectories(model_instance, problem_instance)
        expected = [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]
        
        self.assertTrue(actual.success)
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[0], actual.trajectories[0])]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[1], actual.trajectories[1])]


    def test_evaluate_timecourse_trajectories_with_forcing_inputs(self):
        model_instance, problem_instance = self.do_setup_2p2s_with_forcing_inputs()
        model_instance["model"] = linear_2p2s_mock
        #problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        
        # avoid false negatives
        model_instance["states"] = numpy.multiply(problem_instance["initial_conditions"], 1.1)
        problem_instance["parameters"] = numpy.multiply(problem_instance["parameters"], 1.1)
        problem_instance["inputs"] = numpy.multiply(problem_instance["inputs"], 1.1)
                
        actual = solvers.initial_value.evaluate_timecourse_trajectories(model_instance, problem_instance)
        expected = [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.1, 1.3],
                    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]
        
        self.assertTrue(actual.success)
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[0], actual.trajectories[0])]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected[1], actual.trajectories[1])]


if __name__ == "__main__":
    unittest.main()
