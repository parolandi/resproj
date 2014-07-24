
import unittest

import numpy

import metrics.algebraic
import models.model_data

def linear_mock(x, t, p, u):
    return p[0] * u[0]


def linear_2p2s_mock(p, x):
    assert(len(p) == 2)
    assert(len(x) == 2)
    y = p * x
    return y


class TestAlgebraicMetrics(unittest.TestCase):

    def test_sum_absolute_value_residuals(self):
        values = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
        self.assertEqual(metrics.algebraic.sum_absolute_value_residuals(values), 30)

    
    def test_sum_squared_residuals(self):
        values = [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        def linear(p, x):
            return x
        self.assertEqual(40, metrics.algebraic.sum_squared_residuals([1.0], values, linear, numpy.ones(len(values))))


    def test_residuals_st_linear_2p2s(self):
        offset = 2
        measured = numpy.array([[2.0, 40], [4.0, 80], [6.0, 120]]) + offset

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]
        problem_instance["inputs"] = model_instance["inputs"]

        expected = offset * numpy.ones(measured.shape)
        actual = metrics.algebraic.residuals_st(linear_2p2s_mock, model_instance, problem_instance)
        [self.assertAlmostEqual(exp.all(), act.all(), 8) for exp, act in zip(expected, actual)]


    def test_sum_squared_residuals_st_linear_2p2s_without_dof(self):
        offset = 2
        measured = numpy.array([[2.0, 40], [4.0, 80], [6.0, 120]]) + offset

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]
        problem_instance["inputs"] = model_instance["inputs"]

        expected = offset**2 * measured.size
        dof = []
        actual = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        self.assertAlmostEqual(expected, actual, 8)


    def test_sum_squared_residuals_st_linear_2p2s_with_dof_at_1(self):
        dof_index = 0
        
        offset = 2
        measured = numpy.array([[2.0, 40], [4.0, 80], [6.0, 120]]) + offset

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["parameters"] = [model_instance["parameters"][dof_index]]
        problem_instance["parameter_indices"] = [dof_index]

        expected = offset**2 * measured.size
        dof = numpy.ones(1) * offset
        actual = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        self.assertAlmostEqual(expected, actual, 8)


    def test_sum_squared_residuals_st_linear_2p2s_with_dof_at_2(self):
        dof_index = 1
        
        offset = 4
        measured = numpy.array([[2.0, 40], [4.0, 80], [6.0, 120]]) + offset

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["parameters"] = [model_instance["parameters"][dof_index]]
        problem_instance["parameter_indices"] = [dof_index]

        expected = offset**2 * measured.size
        dof = numpy.ones(1) * offset
        actual = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        self.assertAlmostEqual(expected, actual, 8)


    def test_sum_squared_residuals_st_linear_2p2s_with_dof_at_1and2(self):
        offset = 2
        measured = numpy.array([[1.0, 20], [2.0, 40], [3.0, 60]]) + offset

        model_instance = dict(models.model_data.model_structure)
        # note how these will be overridden by dofs
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["parameter_indices"] = [0, 1]

        expected = offset**2 * measured.size
        # note how these will override the model/problem params
        dof = [1.0, 2.0]
        actual = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        self.assertAlmostEqual(expected, actual, 8)


    def test_sum_squared_residuals_st_linear_2p2s_without_dof_with_output_at_1(self):
        output_index = 0
        offset = 2
        measured = numpy.array([[2.0], [4.0], [6.0]]) + offset

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [output_index]
        problem_instance["inputs"] = model_instance["inputs"]

        expected = offset**2 * measured.size
        dof = []
        actual = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        self.assertAlmostEqual(expected, actual, 8)
        

    def test_sum_squared_residuals_st_linear_2p2s_without_dof_with_output_at_2(self):
        output_index = 1
        offset = 10
        measured = numpy.array([[40], [80], [120]]) + offset

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [output_index]
        problem_instance["inputs"] = model_instance["inputs"]

        expected = offset**2 * measured.size
        dof = []
        actual = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        self.assertAlmostEqual(expected, actual, 8)


    def test_sum_squared_residuals_st_linear_2p2s_with_dof_at_1_and_output_at_1(self):
        dof_index = 0
        output_index = 0
        
        offset = -1
        measured = numpy.array([[1.0], [2.0], [3.0]]) + offset

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = numpy.array([2.0, 4.0])
        model_instance["inputs"] = numpy.array([[1.0, 10], [2.0, 20], [3.0, 30]])

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [output_index]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["parameters"] = [model_instance["parameters"][dof_index]]
        problem_instance["parameter_indices"] = [dof_index]

        expected = offset**2 * measured.size
        dof = [1.0]
        actual = metrics.algebraic.sum_squared_residuals_st(dof, linear_2p2s_mock, model_instance, problem_instance)
        self.assertAlmostEqual(expected, actual, 8)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAlgebraicMetrics)
    unittest.TextTestRunner(verbosity=2).run(suite)
