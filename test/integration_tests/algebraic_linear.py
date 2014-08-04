
import unittest
import numpy

import metrics.algebraic
import metrics.statistical_tests
import models.model_data


def linear_2p2s(p, x):
    assert(len(p) == 2)
    assert(len(x) == 2)
    y = p * x
    return y


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

        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30], [4.0, 40], [5.0, 50], [6.0, 60]])
        problem_instance["inputs"] = model_instance["inputs"]
        offset = -1
        measured = numpy.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]) + offset
        problem_instance["outputs"] = measured
        res = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s, model_instance, problem_instance)
        chi_dof = len(measured) - len(problem_instance["parameter_indices"])
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            res, chi_dof, 0.90)
        self.assertTrue(actual)
        offset = 2
        measured = numpy.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]) + offset
        problem_instance["outputs"] = measured
        res = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s, model_instance, problem_instance)
        chi_dof = len(measured) - len(problem_instance["parameter_indices"])
        actual = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            res, chi_dof, 0.90)
        # three measurements are not fine...
        self.assertFalse(actual)

        
if __name__ == "__main__":
    unittest.main()