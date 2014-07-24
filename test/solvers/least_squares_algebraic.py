
import unittest
import numpy

import solvers.least_squares
import metrics.algebraic
import models.model_data


def linear_2p2s_mock(p, x):
    assert(len(p) == 2)
    assert(len(x) == 2)
    y = p * x
    return y


class TestTestLeastSquaresSolversWithAlgebraicModels(unittest.TestCase):


    def test_solve_slsqp_st_linear_2p2s(self):
        measured = numpy.array([[2.0, 40], [4.0, 80], [6.0, 120]])

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([1.0, 1.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["parameter_indices"] = [0, 1]

        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        algorithm_instance["method"] = 'SLSQP'
        algorithm_instance["initial_guesses"] = numpy.array([1.0, 1.0])

        expected = numpy.array([2.0, 4.0])
        result = solvers.least_squares.solve_slsqp_st( \
            metrics.algebraic.sum_squared_residuals_st, linear_2p2s_mock, model_instance, problem_instance, algorithm_instance)
        actual = result.x
        self.assertAlmostEqual(expected.all(), actual.all(), 8)


if __name__ == "__main__":
    unittest.main()
