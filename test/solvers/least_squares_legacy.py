
import unittest
import numpy

import solvers.least_squares
import metrics.ordinary_differential_legacy
import models.model_data


def linear_mock(x, t, p, u):
    return p[0] * u[0]


class TestLeastSquaresLegacySolvers(unittest.TestCase):


    def test_solve_st(self):
        measured = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = [0.0]
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0]
        problem_instance["parameter_indices"] = [0]
        problem_instance["inputs"] = [1.0]
        problem_instance["outputs"] = measured
        
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0
        
        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        algorithm_instance["method"] = 'SLSQP'
        algorithm_instance["initial_guesses"] = numpy.array([0.1])

        expected = 1.0
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential_legacy.simple_sum_squared_residuals_st, linear_mock, model_instance, problem_instance, algorithm_instance)
        actual = result.x
        self.assertAlmostEqual(expected, actual, 8)
        
        
if __name__ == "__main__":
    unittest.main()