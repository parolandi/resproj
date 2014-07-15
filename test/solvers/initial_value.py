
import unittest

import numpy

import common.utilities
import solvers.initial_value
import models.ordinary_differential

# states, time, parameters, inputs
def linear_mock(x, t, p, u):
    return p[0] * u[0]


def linear_mock_st(y, t, instance):
    instance["states"] = y
    instance["time"] = t
    return instance["parameters"][0] * instance["inputs"][0]


class TestInitialValueSolvers(unittest.TestCase):

    def test_solve_lsoda(self):
        times = numpy.arange(0.0, 1.0, 1.0 / 10)
        param = 1.0
        inputf = 1.0
        initc = 0.0
        result, stuff = solvers.initial_value.solve_lsoda(linear_mock, initc, times, [param], [inputf])
        actual = common.utilities.sliceit(result)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]

    
    def test_solve_lsoda_st(self):
        problem_instance = dict(models.ordinary_differential.problem_structure)
        problem_instance["initial_conditions"] = 0.0
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        model_instance = dict(models.ordinary_differential.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0
        result, stuff = solvers.initial_value.solve_lsoda_st(linear_mock, model_instance, problem_instance)
        actual = common.utilities.sliceit(result)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]

      
    def test_compute_trajectory(self):
        times = numpy.arange(0.0, 1.0, 1.0 / 10)
        param = [1.0]
        inputf = [1.0]
        initc = 0.0
        actual = solvers.initial_value.compute_trajectory(param, linear_mock, initc, inputf, times)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]


    def test_compute_trajectory_st(self):
        problem_instance = dict(models.ordinary_differential.problem_structure)
        problem_instance["initial_conditions"] = 0.0
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        model_instance = dict(models.ordinary_differential.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0
        actual = solvers.initial_value.compute_trajectory_st(linear_mock, model_instance, problem_instance)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInitialValueSolvers)
    unittest.TextTestRunner(verbosity=2).run(suite)
