
import unittest

import numpy

import metrics.ordinary_differential
import models.ordinary_differential

def linear_mock(x, t, p, u):
    return p[0] * u[0]


class TestOrdinaryDifferentialMetrics(unittest.TestCase):

    def test_residuals_st(self):
        measured = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        
        problem_instance = dict(models.ordinary_differential.problem_structure)
        problem_instance["initial_conditions"] = 0.0
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        problem_instance["outputs"] = measured
        model_instance = dict(models.ordinary_differential.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        expected = numpy.zeros(len(measured))
        actual = metrics.ordinary_differential.residuals_st(linear_mock, model_instance, problem_instance)
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]


    def test_sum_squared_residuals_st(self):
        measured = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        
        problem_instance = dict(models.ordinary_differential.problem_structure)
        problem_instance["initial_conditions"] = 0.0
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        problem_instance["outputs"] = measured
        model_instance = dict(models.ordinary_differential.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        expected = 0.0
        dof = model_instance["parameters"]
        actual = metrics.ordinary_differential.sum_squared_residuals_st(dof, linear_mock, model_instance, problem_instance)
        self.assertAlmostEqual(expected, actual, 8)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOrdinaryDifferentialMetrics)
    unittest.TextTestRunner(verbosity=2).run(suite)
