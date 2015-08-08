
import unittest
import setups.kremlingetal_bioreactor as skb

import copy
import logging
import numpy
import time

import common.diagnostics as codi
import common.environment as coen
import metrics.ordinary_differential as mo
import results.plot_tiles as rpt
import solvers.initial_value as si
import solvers.least_squares as sl
import solvers.monte_carlo_multiple_least_squares as smls
import solvers.solver_data as sd
import solvers.solver_utils as sosout


'''
TODO
'''
class TestExperiment04(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment04, self).__init__(*args, **kwargs)
        self.plotting = coen.get_doing_plotting()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-04: start")
        logging.info(codi.get_date_and_time())
        self.model_key = "modelB"


    def __del__(self):
        logging.info("exp-04: finish")
        logging.info(codi.get_date_and_time())
        

    '''
    Simulate at nominal point and plot fit 
    '''
    def test_simulate(self):
        model_data = skb.do_model_setup_model_B()
        published_data = skb.do_get_published_data_spliced_111111()
        problem_data = skb.do_problem_setup(model_data, published_data["calib"])
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
        data_instance = skb.do_get_published_data_spliced_111111()
        problem_data = skb.do_problem_setup(model_data, data_instance["calib"])

        actual = mo.sum_squared_residuals_st(None, None, model_data, problem_data)
        expected = 0.045095700772591826
        self.assertAlmostEqual(actual, expected, 12)

    
    '''
    Calibrate using experimental data 
    '''
    def test_calibrate(self):
        model_data = skb.do_model_setup_model_B()
        data_instance = skb.do_get_published_data_spliced_111111()
        problem_data = skb.do_problem_setup(model_data, data_instance["calib"])
        labels = skb.do_labels()

        ssr_raw = mo.sum_squared_residuals_st(None, None, model_data, problem_data)
        trajectories_raw = si.compute_timecourse_trajectories(None, model_data, problem_data)

        algo_data = dict(sd.algorithm_structure)
        initial_guesses = []
        for ii in range(len(problem_data["parameter_indices"])):
            initial_guesses.append(model_data["parameters"][problem_data["parameter_indices"][ii]])
        algo_data["initial_guesses"] = copy.deepcopy(initial_guesses) 
        logger = sosout.DecisionVariableLogger()
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
        expected = 0.020948695742714324
        self.assertAlmostEqual(actual, expected, 12)
        # TODO add regression test point


    '''
    Calibrate using experimental data; use globalisation 
    '''
    def test_calibrate_global(self):
        model_data = skb.do_model_setup_model_B()
        data_instance = skb.do_get_published_data_spliced_111111()
        problem_data = skb.do_problem_setup(model_data, data_instance["calib"])
        labels = skb.do_labels()
        
        ssr_raw = mo.sum_squared_residuals_st(None, None, model_data, problem_data)
        trajectories_raw = si.compute_timecourse_trajectories(None, model_data, problem_data)

        nom_param_vals = []
        for ii in range(len(problem_data["parameter_indices"])):
            nom_param_vals.append(model_data["parameters"][problem_data["parameter_indices"][ii]])
        
        algorithm = dict(smls.montecarlo_multiple_optimisation_params)
        algorithm["number_of_trials"] = 5
        algorithm["decision_variable_ranges"] = [(0,7.23232059e-05*10), (0,6.00000000e+06*10), (0,1.67959956e-02*10), (0,1.00866368e-02*10)]
        algorithm["subsolver_params"]["method"] = "Nelder-Mead"

        wall_time0 = time.time()
        result = smls.montecarlo_multiple_least_squares(model_data, problem_data, algorithm)
        wall_time = time.time() - wall_time0
        opt_param_est = result["global"]["decision_variables"]
        
        trajectories_fit = si.compute_timecourse_trajectories(None, model_data, problem_data)
        ssr_fit = mo.sum_squared_residuals_st(opt_param_est, None, model_data, problem_data)

        smls.print_montecarlo_multiple_least_squares(wall_time, result, nom_param_vals, ssr_raw, ssr_fit)
        if self.do_plotting:
            rpt.plot_fit(problem_data["time"], problem_data["outputs"], problem_data["time"], trajectories_raw[1:], labels[1:], self.model_key)
            rpt.plot_fit(problem_data["time"], problem_data["outputs"], problem_data["time"], trajectories_fit[1:], labels[1:], self.model_key)

        self.assertTrue(len(result["local"]) == 4)
        actual = result["global"]["objective_function"]
        expected = 0.0211884015947
        self.assertAlmostEquals(actual, expected, 12)
        actual = result["global"]["decision_variables"]
        expected = numpy.array([7.00689640e-05, 7.02472058e+06, 7.04011203e-03, 1.28695959e-01])
        deltas = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-01])
        [self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]


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
