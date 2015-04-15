
import unittest

import copy
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


    def do_setup_single(self):
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = numpy.array([0.0, 1.0])
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["output_indices"] = [0, 1]
        problem_instance["parameters"] = [1.0, 0.5]
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["inputs"] = numpy.array([1.0, 2.0])
        
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0
        model_instance["model"] = linear_2p2s_mock

        return model_instance, problem_instance


    def do_get_measured(self, offset):
        return numpy.asarray([[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], \
                             [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]]) + offset


    def do_get_experiment(self, offset):
        experiment = {}
        experiment["initial_condition_measurements"] = numpy.array([0.0, 1.0])
        experiment["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        experiment["input_measurements"] = numpy.array([1.0, 2.0])
        measured = self.do_get_measured(offset)
        experiment["output_measurements"] = measured
        return experiment
    

    def do_setup_multiple_1(self):
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["output_indices"] = [0, 1]
        problem_instance["parameters"] = [1.0, 0.5]
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["experiments"] = [self.do_get_experiment(1.0)]
        
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        #model_instance["inputs"] = problem_instance["inputs"]
        #model_instance["states"] = problem_instance["initial_conditions"]
        #model_instance["time"] = 0.0
        model_instance["model"] = linear_2p2s_mock
        model_instance["inputs"] = copy.deepcopy(problem_instance["experiments"][0]["input_measurements"])
        model_instance["states"] = copy.deepcopy(problem_instance["experiments"][0]["initial_condition_measurements"])

        return model_instance, problem_instance

    
    def do_setup_multiple_2(self):
        model_instance, problem_instance = self.do_setup_multiple_1()
        problem_instance["experiments"].append(self.do_get_experiment(1.0))
        return model_instance, problem_instance

    
    # test residual trajectories, single experiment
    def test_residuals_single_experiment_linear_2p2s(self):
        model_instance, problem_instance = self.do_setup_single()
        problem_instance["outputs"] = self.do_get_measured(1.0)
        
        expected = numpy.ones(self.do_get_measured(0).shape)
        actual = metrics.ordinary_differential.residuals(model_instance, problem_instance)
        [[self.assertAlmostEqual(exp, act, 8) for exp, act in zip(exps, acts)] for exps, acts in zip(expected, actual)]


    # test residual trajectories, multiple experiments, just one
    def test_residuals_multiple_1_experiments_linear_2p2s(self):
        model_instance, problem_instance = self.do_setup_multiple_1()

        expected = numpy.ones(self.do_get_measured(0).shape)
        actual = metrics.ordinary_differential.residuals(model_instance, problem_instance)
        [[self.assertAlmostEqual(exp, act, 8) for exp, act in zip(exps, acts)] for exps, acts in zip(expected, actual)]


    # test residual trajectories, multiple experiments, this time is two
    def test_residuals_multiple_2_experiments_linear_2p2s(self):
        model_instance, problem_instance = self.do_setup_multiple_2()
        
        expected = numpy.ones(self.do_get_measured(0).shape)
        actual = metrics.ordinary_differential.residuals(model_instance, problem_instance)
        [[self.assertAlmostEqual(exp, act, 8) for exp, act in zip(exps, acts)] for exps, acts in zip(expected, actual)]


if __name__ == "__main__":
    unittest.main()