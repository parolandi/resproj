
import unittest

import numpy

import common.utilities
import solvers.initial_value
import models.model_data
import models.ordinary_differential

# states, time, parameters, inputs
def linear_mock(x, t, p, u):
    return p[0] * u[0]


def linear_mock_st(y, t, instance):
    instance["states"] = y
    instance["time"] = t
    return instance["parameters"][0] * instance["inputs"][0]


class TestInitialValueSolvers(unittest.TestCase):

    def test_solve_lsoda(self):
        times = numpy.arange(0.0, 1.0, 1.0 / 10)
        param = 1.0
        inputf = 1.0
        initc = 0.0
        result, stuff = solvers.initial_value.solve_lsoda(linear_mock, initc, times, [param], [inputf])
        actual = common.utilities.sliceit_assnapshot(result)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]

    
    def test_solve_lsoda_st(self):
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = 0.0
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0
        result, stuff = solvers.initial_value.solve_lsoda_st(linear_mock, model_instance, problem_instance)
        actual = common.utilities.sliceit_assnapshot(result)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]

      
    def test_compute_trajectory(self):
        times = numpy.arange(0.0, 1.0, 1.0 / 10)
        param = [1.0]
        inputf = [1.0]
        initc = 0.0
        actual = solvers.initial_value.compute_trajectory(param, linear_mock, initc, inputf, times)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]


    def test_compute_trajectory_st(self):
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = 0.0
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0
        actual = solvers.initial_value.compute_trajectory_st(linear_mock, model_instance, problem_instance)
        expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        [self.assertAlmostEqual(exp, act, 8) for exp, act in zip(expected, actual)]


    def do_test_epo_receptor_solve_steady_state(self, model):
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
        problem_instance["initial_conditions"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_states))
        problem_instance["initial_conditions"][models.ordinary_differential.states_i["Epo"]] = 2030.19
        problem_instance["initial_conditions"][models.ordinary_differential.states_i["EpoR"]] = 516
        times = numpy.arange(0.0, 5000.0, 500.0)
        problem_instance["time"] = times
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["states"] = model_instance["states"]
        result = solvers.initial_value.compute_trajectory_st(model, model_instance, problem_instance)
        steady_state = result[len(times)-1] 
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
        [self.assertAlmostEquals(actual[key], expected[key], 2) for key in models.ordinary_differential.epo_receptor_states.keys()]

    
    def do_test_epo_receptor_solve_time_course(self, model):
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
        problem_instance["initial_conditions"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_states))
        problem_instance["initial_conditions"][models.ordinary_differential.states_i["Epo"]] = 2030.19
        problem_instance["initial_conditions"][models.ordinary_differential.states_i["EpoR"]] = 516
        times = numpy.arange(0.0, 1500.0, 100.0)
        problem_instance["time"] = times
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["states"] = model_instance["states"]
        result = solvers.initial_value.compute_trajectory_st(model, model_instance, problem_instance)
        snapshots = numpy.asarray(result)
        trajectories = numpy.transpose(snapshots)
        actual = dict(models.ordinary_differential.epo_receptor_states)
        for item in models.ordinary_differential.states_i.items():
            key = item[0]
            index = item[1]
            actual[key] = trajectories[index]
        expected = dict(models.ordinary_differential.epo_receptor_states)
        # copasi result @times=0:1500:100
        expected["Epo"] = numpy.asarray([2030.19, 638.782, 155.361, 37.5639, 10.2865, 2.90606, 0.82607, 0.235169, 0.0669758, 0.0190769,  0.00543388, 0.00154781, 0.000440884, 0.000125583, 3.57718E-005, 1.01894E-005])
        [self.assertAlmostEquals(act, exp, 3) for act, exp in zip(actual["Epo"], expected["Epo"])]


    def test_epo_receptor_solve_steady_state(self):
        self.do_test_epo_receptor_solve_steady_state(models.ordinary_differential.epo_receptor)
        self.do_test_epo_receptor_solve_steady_state(models.ordinary_differential.epo_receptor_nonneg)


    def test_epo_receptor_solve_time_course(self):
        self.do_test_epo_receptor_solve_time_course(models.ordinary_differential.epo_receptor)
        self.do_test_epo_receptor_solve_time_course(models.ordinary_differential.epo_receptor_nonneg)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInitialValueSolvers)
    unittest.TextTestRunner(verbosity=2).run(suite)