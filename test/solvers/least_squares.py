
import unittest
import solvers.least_squares as testme

import copy
import numpy

import metrics.ordinary_differential as meordi
import models.model_data as momoda
import solvers.solver_data as sosoda
import solvers.solver_utils as sosout


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    dx_dt = p * u
    return dx_dt


def callbackit(x):
    print("unit-test: calling-back")


# TODO: test all algorithms with this simple case, non only SLSQP
# TODO: regress with noise
class TestLeastSquaresSolvers(unittest.TestCase):


    def do_setup(self):
        measured = numpy.asarray([[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], \
                                 [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]])
        
        problem_instance = dict(momoda.problem_structure)
        problem_instance["initial_conditions"] = numpy.array([0.0, 1.0])
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = numpy.array([0.1, 10])
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["inputs"] = numpy.array([1.0, 2.0])
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]

        model_instance = dict(momoda.model_structure)
        model_instance["parameters"] = copy.deepcopy(problem_instance["parameters"])
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        algorithm_instance = dict(sosoda.algorithm_structure)
        algorithm_instance["initial_guesses"] = problem_instance["parameters"]

        return model_instance, problem_instance, algorithm_instance


    def test_solve_st_linear_2p2s_include_initial(self):
        model_instance, problem_instance, algorithm_instance = self.do_setup()
        algorithm_instance["method"] = 'SLSQP'
        
        result = testme.solve_st( \
            meordi.sum_squared_residuals_st, linear_2p2s_mock, \
            model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = numpy.array([1.0, 0.5])
        [self.assertAlmostEqual(exp, act, 6) for exp, act in zip(estimate_expected, estimate_actual)]
        
        sum_sq_res_actual = meordi.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        sum_sq_res_expected = 0.0
        self.assertAlmostEqual(sum_sq_res_expected, sum_sq_res_actual, 6)


    def test_solve_st_linear_2p2s_with_mock_callback(self):
        model_instance, problem_instance, algorithm_instance = self.do_setup()
        algorithm_instance["method"] = 'Nelder-Mead'
        algorithm_instance["callback"] = callbackit
        
        result = testme.solve_st( \
            meordi.sum_squared_residuals_st, linear_2p2s_mock, \
            model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = numpy.array([1.000011, 0.5000155])
        [self.assertAlmostEqual(exp, act, 6) for exp, act in zip(estimate_expected, estimate_actual)]
        
        sum_sq_res_actual = meordi.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        sum_sq_res_expected = 0.0
        self.assertAlmostEqual(sum_sq_res_expected, sum_sq_res_actual, 6)


    # TODO: move into integration tests; this is not a unit-test
    def test_solve_st_linear_2p2s_with_object_callback(self):
        model_instance, problem_instance, algorithm_instance = self.do_setup()
        algorithm_instance["method"] = 'Nelder-Mead'
        logger = sosout.DecisionVariableLogger()
        algorithm_instance["callback"] = logger.log_decision_variables
        
        result = testme.solve_st( \
            meordi.sum_squared_residuals_st, linear_2p2s_mock, \
            model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = numpy.array([1.000011, 0.5000155])
        [self.assertAlmostEqual(exp, act, 6) for exp, act in zip(estimate_expected, estimate_actual)]
        
        sum_sq_res_actual = meordi.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        sum_sq_res_expected = 0.0
        self.assertAlmostEqual(sum_sq_res_expected, sum_sq_res_actual, 6)


    def test_solve_st_linear_2p2s_exclude_initial(self):
        model_instance, problem_instance, algorithm_instance = self.do_setup()
        algorithm_instance["method"] = 'SLSQP'
        problem_instance["outputs"][0][0] = 10
        problem_instance["outputs"][1][0] = 10
        # with these tampered-with values, only "exclude" succeeds
        problem_instance["initial"] = "exclude"
        
        result = testme.solve_st( \
            meordi.sum_squared_residuals_st, linear_2p2s_mock, \
            model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = numpy.array([1.0, 0.5])
        [self.assertAlmostEqual(exp, act, 6) for exp, act in zip(estimate_expected, estimate_actual)]
        
        sum_sq_res_actual = meordi.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        sum_sq_res_expected = 0.0
        self.assertAlmostEqual(sum_sq_res_expected, sum_sq_res_actual, 6)
        
    
    def test_solve_st_linear_2p2s_1dof_include_initial(self):
        model_instance, problem_instance, algorithm_instance = self.do_setup()
        algorithm_instance["method"] = 'SLSQP'
        
        model_instance["parameters"][1] = 0.5
        problem_instance["parameters"] = [0.1]
        problem_instance["parameter_indices"] = [0]
        algorithm_instance["initial_guesses"] = [copy.deepcopy(problem_instance["parameters"][0])]
                
        result = testme.solve_st( \
            meordi.sum_squared_residuals_st, linear_2p2s_mock, \
            model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = [1.0]
        [self.assertAlmostEqual(exp, act, 5) for exp, act in zip(estimate_expected, estimate_actual)]
        
        sum_sq_res_actual = meordi.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        sum_sq_res_expected = 0.0
        self.assertAlmostEqual(sum_sq_res_expected, sum_sq_res_actual, 6)
    

    def test_solve_st_linear_2p2s_1dof_include_initial_model_and_metric_are_not_none(self):
        model_instance, problem_instance, algorithm_instance = self.do_setup()
        model_instance["model"] = linear_2p2s_mock
        problem_instance["performance_measure"] = meordi.sum_squared_residuals_st
        algorithm_instance["method"] = 'SLSQP'
        
        model_instance["parameters"][1] = 0.5
        problem_instance["parameters"] = [0.1]
        problem_instance["parameter_indices"] = [0]
        algorithm_instance["initial_guesses"] = [copy.deepcopy(problem_instance["parameters"][0])]
                
        result = testme.solve_st(None, None, model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = [1.0]
        [self.assertAlmostEqual(exp, act, 5) for exp, act in zip(estimate_expected, estimate_actual)]
        
        sum_sq_res_actual = meordi.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        sum_sq_res_expected = 0.0
        self.assertAlmostEqual(sum_sq_res_expected, sum_sq_res_actual, 6)


    def test_solve_linear_2p2s_1dof_include_initial_model_and_metric_are_not_none(self):
        model_instance, problem_instance, algorithm_instance = self.do_setup()
        model_instance["model"] = linear_2p2s_mock
        problem_instance["performance_measure"] = meordi.sum_squared_residuals_st
        algorithm_instance["method"] = 'SLSQP'
        
        model_instance["parameters"][1] = 0.5
        problem_instance["parameters"] = [0.1]
        problem_instance["parameter_indices"] = [0]
        algorithm_instance["initial_guesses"] = [copy.deepcopy(problem_instance["parameters"][0])]
                
        result = testme.solve(model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = [1.0]
        [self.assertAlmostEqual(exp, act, 5) for exp, act in zip(estimate_expected, estimate_actual)]
        
        sum_sq_res_actual = meordi.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        sum_sq_res_expected = 0.0
        self.assertAlmostEqual(sum_sq_res_expected, sum_sq_res_actual, 6)


if __name__ == "__main__":
    unittest.main()
