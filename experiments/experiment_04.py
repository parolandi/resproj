
import unittest
import setups.kremlingetal_bioreactor as skb

import copy
import numpy
import time

import common.utilities as cu
import metrics.ordinary_differential as mo
import models.model_data
#import results.plot as rps
import results.plot_tiles as rpt
import solvers.initial_value as si
import solvers.least_squares as sl
import solvers.monte_carlo_multiple_least_squares as smls
import solvers.solver_data as sd


class TestExperiment04(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment04, self).__init__(*args, **kwargs)
        self.do_plotting = False
        self.model_key = "modelB"
        

    '''
    Simulate at nominal point and plot fit 
    '''
    def test_simulate(self):
        model_data = skb.do_model_setup_model_B()
        problem_data = skb.do_problem_setup(model_data)
        labels = skb.do_labels()

        trajectories = si.compute_timecourse_trajectories(None, model_data, problem_data)
        
        if self.do_plotting:
            rpt.plot_fit(problem_data["time"], problem_data["outputs"], problem_data["time"], trajectories[1:], labels[1:], self.model_key)
        
        endpoint = len(trajectories[0])-1
        actual = [trajectories[ii][endpoint] for ii in range(1, len(trajectories))]
        expected = [0.39384222, 0.07740635, 0.23982609, 0.01189731, 0.03081916]
        [self.assertAlmostEquals(act, exp) for act, exp in zip(actual, expected)]


    '''
    Compute sum squared residuals 
    '''
    def test_metric(self):
        model_data = skb.do_model_setup_model_B()
        problem_data = skb.do_problem_setup(model_data)

        actual = mo.sum_squared_residuals_st(None, None, model_data, problem_data)
        expected = 0.045095700772591826
        self.assertAlmostEqual(actual, expected, 12)

    
    '''
    Calibrate using experimental data 
    '''
    def test_calibrate(self):
        model_data = skb.do_model_setup_model_B()
        problem_data = skb.do_problem_setup(model_data)
        labels = skb.do_labels()

        ssr_raw = mo.sum_squared_residuals_st(None, None, model_data, problem_data)
        trajectories_raw = si.compute_timecourse_trajectories(None, model_data, problem_data)

        algo_data = dict(sd.algorithm_structure)
        initial_guesses = []
        for ii in range(len(problem_data["parameter_indices"])):
            initial_guesses.append(model_data["parameters"][problem_data["parameter_indices"][ii]])
        algo_data["initial_guesses"] = copy.deepcopy(initial_guesses) 
        logger = sl.DecisionVariableLogger()
        algo_data["callback"] = logger.log_decision_variables
        algo_data["method"] = 'Nelder-Mead'

        result = sl.solve(model_data, problem_data, algo_data)
        problem_data["parameters"] = result.x
        # need to do this here because problem data is kind of ignored
        for ii in range(len(problem_data["parameter_indices"])):
            model_data["parameters"][problem_data["parameter_indices"][ii]] = result.x[ii]

        trajectories_fit = si.compute_timecourse_trajectories(None, model_data, problem_data)
        ssr_fit = mo.sum_squared_residuals_st(result.x, None, model_data, problem_data)
                
        print("initial guesses:    ", initial_guesses)
        print("parameter estimates:", result.x.tolist())
        print("ssr (raw):          ", ssr_raw)        
        print("ssr (fit):          ", ssr_fit)
        if self.do_plotting:
            rpt.plot_fit(problem_data["time"], problem_data["outputs"], problem_data["time"], trajectories_raw[1:], labels[1:], self.model_key)
            rpt.plot_fit(problem_data["time"], problem_data["outputs"], problem_data["time"], trajectories_fit[1:], labels[1:], self.model_key)
            
        actual = ssr_fit
        expected = 0.020948632939275735
        self.assertAlmostEqual(actual, expected, 12)
        # TODO add regression test point


    '''
    Calibrate using experimental data; use globalisation 
    '''
    def test_calibrate_global(self):
        model_data = skb.do_model_setup_model_B()
        problem_data = skb.do_problem_setup(model_data)
        labels = skb.do_labels()
        
        ssr_raw = mo.sum_squared_residuals_st(None, None, model_data, problem_data)
        trajectories_raw = si.compute_timecourse_trajectories(None, model_data, problem_data)

        nom_param_vals = []
        for ii in range(len(problem_data["parameter_indices"])):
            nom_param_vals.append(model_data["parameters"][problem_data["parameter_indices"][ii]])
        
        algorithm = dict(smls.montecarlo_multiple_optimisation_params)
        algorithm["number_of_trials"] = 5
        algorithm["decision_variable_ranges"] = [(0,7.23232059e-05*10), (0,6.00000000e+06*10), (0,1.00000000e+01*10), (0,1.67959956e-02*10), (0,1.00866368e-02*10)]
        algorithm["subsolver_params"]["method"] = "Nelder-Mead"

        wall_time0 = time.time() 
        result = smls.montecarlo_multiple_least_squares(model_data, problem_data, algorithm)
        wall_time = time.time() - wall_time0
        opt_param_est = result["global"]["decision_variables"]
        
        trajectories_fit = si.compute_timecourse_trajectories(None, model_data, problem_data)
        ssr_fit = mo.sum_squared_residuals_st(opt_param_est, None, model_data, problem_data)

        print("wall time:", wall_time)
        print("number of local optima:     ", len(result["local"]))
        print("nominal parameter values:   ", nom_param_vals)
        print("optimal parameter estimates:", opt_param_est.tolist())
        print("ssr (raw):                  ", ssr_raw)        
        print("ssr (fit):                  ", ssr_fit)        
        if self.do_plotting:
            rpt.plot_fit(problem_data["time"], problem_data["outputs"], problem_data["time"], trajectories_raw[1:], labels[1:], self.model_key)
            rpt.plot_fit(problem_data["time"], problem_data["outputs"], problem_data["time"], trajectories_fit[1:], labels[1:], self.model_key)

        self.assertTrue(len(result["local"]) == 3)
        actual = result["global"]["objective_function"]
        expected = 0.021119404945328022
        self.assertAlmostEquals(actual, expected, 12)


if __name__ == "__main__":
    run_slow_tests = False
    suite = unittest.TestSuite()
    suite.addTest(TestExperiment04("test_simulate"))
    suite.addTest(TestExperiment04("test_metric"))
    suite.addTest(TestExperiment04("test_calibrate"))
    if run_slow_tests:
        suite.addTest(TestExperiment04("test_calibrate_global"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
