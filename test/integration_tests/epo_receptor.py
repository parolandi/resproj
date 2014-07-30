
import unittest
import numpy

import metrics.ordinary_differential
import models.model_data
import models.ordinary_differential
import solvers.initial_value
import solvers.least_squares
import solvers.nonlinear_algebraic


class Test(unittest.TestCase):

    # steady-state as nonlinear algebraic boilerplate
    def do_test_epo_receptor_solve_steady_state_nla(self, model, test_numerical_value):
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

    
    # steady-state as ordinary differential boilerplate
    def do_test_epo_receptor_solve_steady_state_ode(self, model):
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

    
    # dynamic/time-course boilerplate
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
        # TODO; enable this assertion
#        assert(len(actual["Epo"]) == len(expected["Epo"]))
        [self.assertAlmostEquals(act, exp, 3) for act, exp in zip(actual["Epo"], expected["Epo"])]


    # least-squares boilerplate
    def do_test_epo_receptor_solve_least_squares(self, numerical_method, offset, expected):
        nominal = numpy.array([0.00010496])
        params = numpy.ones(len(models.ordinary_differential.params_i))
        for par in models.ordinary_differential.params_i.items():
            params[par[1]] = models.ordinary_differential.epo_receptor_default_parameters[par[0]]
        inputs = numpy.ones(len(models.ordinary_differential.inputs_i))
        for inp in models.ordinary_differential.inputs_i.items():
            inputs[inp[1]] = models.ordinary_differential.epo_receptor_default_inputs[inp[0]]
        measured = numpy.asarray([2030.19, 638.782, 155.361, 37.5639, 10.2865, 2.90606, 0.82607, 0.235169, 0.0669758, 0.0190769,  0.00543388, 0.00154781, 0.000440884, 0.000125583, 3.57718E-005, 1.01894E-005])

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = params
        model_instance["inputs"] = inputs
        model_instance["states"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_states))

        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_states))
        problem_instance["initial_conditions"][models.ordinary_differential.states_i["Epo"]] = 2030.19
        problem_instance["initial_conditions"][models.ordinary_differential.states_i["EpoR"]] = 516
        times = numpy.arange(0.0, 1600.0, 100.0)
        problem_instance["time"] = times
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["parameter_indices"] = [models.ordinary_differential.params_i["k_on"]]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["states"] = model_instance["states"]
        problem_instance["outputs"] =  measured
        problem_instance["output_indices"] = [models.ordinary_differential.states_i["Epo"]]
        
        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        algorithm_instance["method"] = numerical_method
        algorithm_instance["initial_guesses"] = nominal + offset

        result = result = solvers.least_squares.solve_slsqp_orddiff_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            models.ordinary_differential.epo_receptor, model_instance, problem_instance, algorithm_instance)
        actual = result.x
        self.assertAlmostEquals(actual, expected, 7)


    # steady-state as nla; two model realisations
    def test_epo_receptor_solve_steady_state_nla(self):
        self.do_test_epo_receptor_solve_steady_state_nla(models.ordinary_differential.epo_receptor, -125.64718517054551)
        self.do_test_epo_receptor_solve_steady_state_nla(models.ordinary_differential.epo_receptor_nonneg, 0.0)

    
    # steady-state as ode; two model realisations
    def test_epo_receptor_solve_steady_state_ode(self):
        self.do_test_epo_receptor_solve_steady_state_ode(models.ordinary_differential.epo_receptor)
        self.do_test_epo_receptor_solve_steady_state_ode(models.ordinary_differential.epo_receptor_nonneg)


    # dynamic/time-course; two model realisations
    def test_epo_receptor_solve_time_course(self):
        self.do_test_epo_receptor_solve_time_course(models.ordinary_differential.epo_receptor)
        self.do_test_epo_receptor_solve_time_course(models.ordinary_differential.epo_receptor_nonneg)

    
    # nelder-mead algorithm; 2oom above
    def test_epo_receptor_solve_least_squares_neldermead_p2oom(self):
        self.do_test_epo_receptor_solve_least_squares('Nelder-Mead', 0.01, 0.00010496)
        
    
    # powell algorithm; 2oom above
    def test_epo_receptor_solve_least_squares_powell_p2oom(self):
        self.do_test_epo_receptor_solve_least_squares('Powell', 0.01, 1.18865310)
        
    
    # l-bfgs-b algorithm; 2oom above
    def test_epo_receptor_solve_least_squares_lbfgsb_p2oom(self):
        self.do_test_epo_receptor_solve_least_squares('L-BFGS-B', 0.01, 0.00469798)
        
    
    # tnc algorithm; 2oom above
    def test_epo_receptor_solve_least_squares_tnc_p2oom(self):
        self.do_test_epo_receptor_solve_least_squares('TNC', 0.01, 0.00010496)

    
    # nelder-mead algorithm; 2oom below
    def test_epo_receptor_solve_least_squares_neldermead_m2oom(self):
        self.do_test_epo_receptor_solve_least_squares('Nelder-Mead', -0.000103, 0.00010496)
        
    
    # powell algorithm; 2oom below
    def test_epo_receptor_solve_least_squares_powell_m2oom(self):
        self.do_test_epo_receptor_solve_least_squares('Powell', -0.000103, 0.93299266)
        
    
    # l-bfgs-b algorithm; 2oom below
    def test_epo_receptor_solve_least_squares_lbfgsb_m2oom(self):
        self.do_test_epo_receptor_solve_least_squares('L-BFGS-B', -0.000103, 0.00010496)
        
    
    # tnc algorithm; 2oom below
    def test_epo_receptor_solve_least_squares_tnc_m2oom(self):
        self.do_test_epo_receptor_solve_least_squares('TNC', -0.000103, 0.00010496)


if __name__ == "__main__":
    unittest.main()
