
import unittest
import numpy

import metrics.ordinary_differential
import models.model_data


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    dx_dt = p * u
    return dx_dt


class TestOrdinaryDifferentialMetrics(unittest.TestCase):

    def test_residuals_st_linear_2p2s(self):
        offset = 1.0
        measured = numpy.asarray([[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], \
                                 [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]) + offset
        
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = numpy.array([0.0, 1.0])
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0, 0.5]
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["inputs"] = numpy.array([1.0, 2.0])
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        expected = numpy.ones(measured.shape)
        actual = metrics.ordinary_differential.residuals_st(linear_2p2s_mock, model_instance, problem_instance)
        [[self.assertAlmostEqual(exp, act, 8) for exp, act in zip(exps, acts)] for exps, acts in zip(expected, actual)]


    def test_sum_squared_residuals_st_linear_2p2s(self):
        offset = 3.0
        measured = numpy.asarray([[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], \
                                 [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]) + offset
        
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = numpy.array([0.0, 1.0])
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0, 0.5]
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["inputs"] = numpy.array([1.0, 2.0])
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        dof = []
        actual = metrics.ordinary_differential.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        expected = offset**2 * measured.size
        self.assertAlmostEqual(expected, actual, 8)

    
    def test_sum_squared_residuals_st_linear_2p2s_with_1output(self):
        offset = 3.0
        measured = numpy.asarray([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]) + offset
        
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = numpy.array([0.0, 1.0])
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0, 0.5]
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["inputs"] = numpy.array([1.0, 2.0])
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0]

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        dof = []
        actual = metrics.ordinary_differential.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        expected = offset**2 * measured.size
        self.assertAlmostEqual(expected, actual, 8)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOrdinaryDifferentialMetrics)
    unittest.TextTestRunner(verbosity=2).run(suite)
