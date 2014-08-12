
import unittest
import numpy

import metrics.algebraic
import metrics.confidence_measures
import metrics.statistical_tests
import models.model_data


def linear_2p2s(p, x):
    assert(len(p) == 2)
    assert(len(x) == 2)
    y = p * x
    return y


# returns Jacobian w.r.t. p[0]
def J_linear_2p2s(p, x):
    assert(len(p) == 2)
    assert(len(x) == 2)
    dy0_dp0 = x[0]
    dy1_dp0 = 0.0
    return [dy0_dp0, dy1_dp0]


class TestLinear2p2s(unittest.TestCase):

    def test_linear_2p2s_with_dof_at_1_two_sided_chi_squared(self):
        dof_index = 0
        output_index = 0
        
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["output_indices"] = [output_index]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["parameters"] = [model_instance["parameters"][dof_index]]
        problem_instance["parameter_indices"] = [dof_index]

        dof = [1.0]

        # three measurements
        # one standard deviation
        offset = -1
        measured = numpy.array([[1.0], [2.0], [3.0]]) + offset
        problem_instance["outputs"] = measured       
        res = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s, model_instance, problem_instance)
        chi_dof = len(measured) - len(problem_instance["parameter_indices"])
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            res, chi_dof, 0.90)
        self.assertTrue(actual)
        # two standard deviations
        offset = 2
        measured = numpy.array([[1.0], [2.0], [3.0]]) + offset
        problem_instance["outputs"] = measured
        res = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s, model_instance, problem_instance)
        chi_dof = len(measured) - len(problem_instance["parameter_indices"])
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            res, chi_dof, 0.90)
        self.assertFalse(actual)

        # six measurements
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30], [4.0, 40], [5.0, 50], [6.0, 60]])
        problem_instance["inputs"] = model_instance["inputs"]
        # one standard deviation
        offset = -1
        measured = numpy.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]) + offset
        problem_instance["outputs"] = measured
        res = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s, model_instance, problem_instance)
        chi_dof = len(measured) - len(problem_instance["parameter_indices"])
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            res, chi_dof, 0.90)
        self.assertTrue(actual)
        # two standard deviations
        offset = 2
        measured = numpy.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]) + offset
        problem_instance["outputs"] = measured
        res = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s, model_instance, problem_instance)
        chi_dof = len(measured) - len(problem_instance["parameter_indices"])
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            res, chi_dof, 0.90)
        # three measurements are not fine...
        self.assertFalse(actual)


    # TODO: test 1p2s
    # TODO: test 2p1s
    def test_linear_2p2s_with_dof_at_1_correlation_matrix(self):
        dof_index = 0
        output_index = 0

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["output_indices"] = [output_index]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["parameters"] = [model_instance["parameters"][dof_index]]
        problem_instance["parameter_indices"] = [dof_index]

        dof = [1.0]
        # one standard deviation
        offset = -1
        measured = numpy.array([[1.0], [2.0], [3.0]]) + offset
        problem_instance["outputs"] = measured
        sens = [J_linear_2p2s([dof[0], model_instance["parameters"][1]], x) for x in model_instance["inputs"]]
        # identity covariance matrix of observation errors
        cov_obs_errs = numpy.identity(3)
        actual = metrics.confidence_measures.compute_covariance_matrix(sens, cov_obs_errs)
        expected = numpy.array([[1**2+2**2+3**2, 0], [0, 0]])
        [[self.assertEqual(act, exp) for act, exp in zip(acts, exps)] for acts, exps in zip(actual, expected)]
        
        # diagonal covariance matrix of observation errors
        multiplier = 2
        cov_obs_errs = numpy.identity(3) * multiplier
        actual = metrics.confidence_measures.compute_covariance_matrix(sens, cov_obs_errs)
        expected = numpy.array([[(1**2+2**2+3**2)/multiplier, 0], [0, 0]])
        [[self.assertEqual(act, exp) for act, exp in zip(acts, exps)] for acts, exps in zip(actual, expected)]

        # TODO: test non-diagonal covariance of observation errors matrix
        # TODO: test non-singular Jacobian matrix


    def test_linear_2p2s_with_dof_at_1_two_sided_t_student(self):
        dof_index = 0
        output_index = 0
        
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["output_indices"] = [output_index]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["parameters"] = [model_instance["parameters"][dof_index]]
        problem_instance["parameter_indices"] = [dof_index]

        dof = [1.0]

        # three measurements
        # one standard deviation
        offset = -1
        measured = numpy.array([[1.0], [2.0], [3.0]]) + offset
        problem_instance["outputs"] = measured       
        # TODO: use this residual to compute the true covariance matrix...
        res = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s, model_instance, problem_instance)
        # ... for the time being use the identity
        cov_obs_errs = numpy.identity(3)
        sens = [J_linear_2p2s([dof[0], model_instance["parameters"][1]], x) for x in model_instance["inputs"]]
        cov_param_est = metrics.confidence_measures.compute_covariance_matrix(sens, cov_obs_errs)
        t_dof = len(measured) - len(problem_instance["parameter_indices"])
        multiplier = 2.91998558036 * 0.99
        param_est_values = cov_param_est[0][0] * multiplier
        actual = metrics.statistical_tests.calculate_two_sided_t_student_test_for_parameter_estimates( \
            param_est_values, cov_param_est[0][0], t_dof, 0.90)
        self.assertFalse(actual)
        multiplier = 2.91998558036 * 1.01
        param_est_values = cov_param_est[0][0] * multiplier
        actual = metrics.statistical_tests.calculate_two_sided_t_student_test_for_parameter_estimates( \
            param_est_values, cov_param_est[0][0], t_dof, 0.90)
        self.assertTrue(actual)


if __name__ == "__main__":
    unittest.main()