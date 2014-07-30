
import unittest

import numpy

import models.model_data
import solvers.solver_data
import solvers.nonlinear_algebraic

def linear_mock(x, t, p, u):
    return p[0] * u[0] - x[0]


def kin_second_order_prod_first_order_deg_mock(x, t, p, u):
    return p[0] * x[0]**2 - p[1] * x[0]


class TestNonlinearAlgebraicSolvers(unittest.TestCase):


    def test_solve_linear(self):
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = [2.0]
        model_instance["inputs"] = [2.0]
        model_instance["states"] = [1.0]
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["inputs"] = model_instance["inputs"]
        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        algorithm_instance["method"] = solvers.solver_data.algorithmic_methods["nonlinear_algebraic"] \
            ["key-hybr-suite-MINPACK-method-modified-Powell-ref-More-Garbow-Hillstrom-aff-ANL"]
        algorithm_instance["initial_guesses"] = numpy.array([1.0])
        algorithm_instance["tolerance"] = 1E-6
        result = solvers.nonlinear_algebraic.solve(linear_mock, model_instance, problem_instance, algorithm_instance)
        actual = result.x
        expected = 4.0
        self.assertAlmostEqual(actual, expected, 8)


    def test_solve_kin(self):
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = [2.0, 1.0]
        model_instance["inputs"] = [0.0]
        model_instance["states"] = [1.0]
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["inputs"] = model_instance["inputs"]
        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        algorithm_instance["method"] = solvers.solver_data.algorithmic_methods["nonlinear_algebraic"] \
            ["key-hybr-suite-MINPACK-method-modified-Powell-ref-More-Garbow-Hillstrom-aff-ANL"]
        algorithm_instance["initial_guesses"] = numpy.array([1.0])
        algorithm_instance["tolerance"] = 1E-6
        result = solvers.nonlinear_algebraic.solve(kin_second_order_prod_first_order_deg_mock, model_instance, problem_instance, algorithm_instance)
        actual = result.x
        expected = 0.5
        self.assertAlmostEqual(actual, expected, 8)

    
if __name__ == "__main__":
    unittest.main()
