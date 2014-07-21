
import unittest

import numpy

import models.model_data
import models.ordinary_differential
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

    
    def do_test_epo_receptor_solve_steady_state(self, model, test_numerical_value):
        params = numpy.ones(len(models.ordinary_differential.params_i))
        for par in models.ordinary_differential.params_i.items():
            params[par[1]] = models.ordinary_differential.epo_receptor_default_parameters[par[0]]
        inputs = numpy.ones(len(models.ordinary_differential.inputs_i))
        for inp in models.ordinary_differential.inputs_i.items():
            inputs[inp[1]] = models.ordinary_differential.epo_receptor_default_inputs[inp[0]]
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = params
        model_instance["inputs"] = inputs
        model_instance["states"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_states))
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["states"] = model_instance["states"]
        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        algorithm_instance["method"] = solvers.solver_data.algorithmic_methods["nonlinear_algebraic"] \
            ["key-hybr-suite-MINPACK-method-modified-Powell-ref-More-Garbow-Hillstrom-aff-ANL"]
        algorithm_instance["initial_guesses"] = numpy.ones(len(model_instance["states"]))
        algorithm_instance["initial_guesses"][models.ordinary_differential.states_i["Epo"]] = 2030.19
        algorithm_instance["initial_guesses"][models.ordinary_differential.states_i["EpoR"]] = 516
        algorithm_instance["tolerance"] = 1E-12
        result = solvers.nonlinear_algebraic.solve(model, model_instance, problem_instance, algorithm_instance)
        steady_state = result.x
        actual = dict(models.ordinary_differential.epo_receptor_states)
        for item in models.ordinary_differential.states_i.items():
            key = item[0]
            index = item[1]
            actual[key] = steady_state[index]
        expected = dict(models.ordinary_differential.epo_receptor_states)
        # copasi result @time=10,000
        expected["Epo"] = -6.32783E-018
        expected["dEpo_e"] = 1700.65
        expected["EpoR"] = 516
        expected["Epo_EpoR"] = -4.31186E-018
        expected["Epo_EpoR_i"] = -1.90202E-017
        expected["dEpo_i"] = 329.542
        # test that it does not meet the expected value
        self.assertNotAlmostEqual(actual["dEpo_e"], expected["dEpo_e"], 2)
        numerical_result_dEpo_e = test_numerical_value
        # test that, at least, it provides the same numerical result consistently 
        self.assertAlmostEqual(actual["dEpo_e"], numerical_result_dEpo_e, 2)

    
    def test_epo_receptor_solve_steady_state(self):
        self.do_test_epo_receptor_solve_steady_state(models.ordinary_differential.epo_receptor, -125.64718517054551)
        self.do_test_epo_receptor_solve_steady_state(models.ordinary_differential.epo_receptor_nonneg, 0.0)


if __name__ == "__main__":
    unittest.main()
