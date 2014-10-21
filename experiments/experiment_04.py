
import unittest
import models.kremlingetal_bioreactor as mk

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
import solvers.solver_data as sd

import solvers.monte_carlo_multiple_least_squares as smls


class TestExperiment04(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment04, self).__init__(*args, **kwargs)
        self.do_plotting = False
        self.model_key = "modelB"
        

    def do_config(self, model_key):
        self.model_key = model_key


    def do_get_published_data(self):
        # TODO: handle gracefully
        published_data = open("C:/documents/resproj/bench/data_time_0_20.txt", 'r')
        data = numpy.loadtxt(published_data)
        trajectories_without_V = cu.sliceit_astrajectory(data)
        return trajectories_without_V[0], trajectories_without_V[1:]
        

    def do_setup(self):
        model = self.model_key
        model_func = None
        if model is "modelA":
            model_func = mk.evaluate_modelA
        else:
            model_func = mk.evaluate_modelB
        
        tt = numpy.linspace(0.0, 20.0, 11, endpoint=True)
        
        p = numpy.ones(len(mk.pmap))
        for par in mk.pmap.items():
            p[par[1]] = mk.pvec[par[0]]
        
        u = numpy.ones(len(mk.umap))
        for inp in mk.umap.items():
            u[inp[1]] = mk.uvec_0h[inp[0]]
        
        x = numpy.ones(len(mk.xmap))
        labels = [""] * len(x)
        for ste in mk.xmap.items():
            x[ste[1]] = mk.xvec[ste[0]]
            labels[ste[1]] = ste[0]
        
        model_data = dict(models.model_data.model_structure)
        model_data["parameters"] = copy.deepcopy(p)
        model_data["inputs"] = copy.deepcopy(u)
        model_data["states"] = copy.deepcopy(x)
        
        problem_data = dict(models.model_data.problem_structure)
        problem_data["initial_conditions"] = copy.deepcopy(x)
        problem_data["time"] = tt
        problem_data["parameters"] = copy.deepcopy(p)
        problem_data["inputs"] = copy.deepcopy(u)

        return model_func, model_data, problem_data, labels

    
    '''
    Simulate at nominal point and plot fit 
    '''
    def test_simulate(self):
        model_func, model_data, problem_data, labels = self.do_setup()

        trajectories = si.compute_timecourse_trajectories(model_func, model_data, problem_data)
        time, observations = self.do_get_published_data()
        tt = problem_data["time"]
        
        if self.do_plotting:
            rpt.plot_fit(time, observations, tt, trajectories[1:], labels[1:], self.model_key)
        
        endpoint = len(trajectories[0])-1
        actual = [trajectories[ii][endpoint] for ii in range(1, len(trajectories))]
        expected = [0.39384222, 0.07740635, 0.23982609, 0.01189731, 0.03081916]
        [self.assertAlmostEquals(act, exp) for act, exp in zip(actual, expected)]


    '''
    Compute sum squared residuals 
    '''
    def test_metric(self):
        model_func, model_data, problem_data, _ = self.do_setup()
        _, observations = self.do_get_published_data()

        problem_data["output_indices"] = [1, 2, 3, 4, 5]
        problem_data["outputs"] = observations
        actual = mo.sum_squared_residuals_st(None, model_func, model_data, problem_data)
        expected = 0.045095700772591826
        self.assertAlmostEqual(actual, expected, 12)

    
    '''
    Calibrate using experimental data 
    '''
    def test_calibrate(self):
        model_func, model_data, problem_data, labels = self.do_setup()
        time, observations = self.do_get_published_data()
        
        problem_data["output_indices"] = [1, 2, 3, 4, 5]
        problem_data["outputs"] = observations
        tt = problem_data["time"]
        
        ssr_raw = mo.sum_squared_residuals_st(None, model_func, model_data, problem_data)
        trajectories_raw = si.compute_timecourse_trajectories(model_func, model_data, problem_data)

        problem_data["parameter_indices"] = [0, 3, 5, 8, 9]
        problem_data["parameters"] = numpy.zeros(len(problem_data["parameter_indices"]))
        problem_data["bounds"] = [(0,None), (0,None), (0,None), (0,None), (0,None)]
        
        algo_data = dict(sd.algorithm_structure)
        initial_guesses = []
        for ii in range(len(problem_data["parameter_indices"])):
            initial_guesses.append(model_data["parameters"][problem_data["parameter_indices"][ii]])
        algo_data["initial_guesses"] = copy.deepcopy(initial_guesses) 
        logger = sl.DecisionVariableLogger()
        algo_data["callback"] = logger.log_decision_variables
        algo_data["method"] = 'Nelder-Mead'

        result = sl.solve_st(mo.sum_squared_residuals_st, model_func, model_data, problem_data, algo_data)
        problem_data["parameters"] = result.x
        # need to do this here because problem data is kind of ignored
        for ii in range(len(problem_data["parameter_indices"])):
            model_data["parameters"][problem_data["parameter_indices"][ii]] = result.x[ii]

        trajectories_fit = si.compute_timecourse_trajectories(model_func, model_data, problem_data)
        ssr_fit = mo.sum_squared_residuals_st(result.x, model_func, model_data, problem_data)
                
        print("initial guesses:    ", initial_guesses)
        print("parameter estimates:", result.x.tolist())
        print("ssr (raw):          ", ssr_raw)        
        print("ssr (fit):          ", ssr_fit)
        if self.do_plotting:
            rpt.plot_fit(time, observations, tt, trajectories_raw[1:], labels[1:], self.model_key)
            rpt.plot_fit(time, observations, tt, trajectories_fit[1:], labels[1:], self.model_key)
            
        actual = ssr_fit
        expected = 0.020948632939275735
        self.assertAlmostEqual(actual, expected, 12)
        # TODO add regression test point


    '''
    Calibrate using experimental data; use globalisation 
    '''
    def test_calibrate_global(self):
        model_func, model_data, problem_data, labels = self.do_setup()
        times, observations = self.do_get_published_data()
        
        problem_data["output_indices"] = [1, 2, 3, 4, 5]
        problem_data["outputs"] = observations
        tt = problem_data["time"]
        
        ssr_raw = mo.sum_squared_residuals_st(None, model_func, model_data, problem_data)
        trajectories_raw = si.compute_timecourse_trajectories(model_func, model_data, problem_data)

        problem_data["parameter_indices"] = [0, 3, 5, 8, 9]
        problem_data["parameters"] = numpy.zeros(len(problem_data["parameter_indices"]))
        problem_data["bounds"] = [(0,None), (0,None), (0,None), (0,None), (0,None)]
        model_data["model"] = model_func
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
        
        trajectories_fit = si.compute_timecourse_trajectories(model_func, model_data, problem_data)
        ssr_fit = mo.sum_squared_residuals_st(opt_param_est, model_func, model_data, problem_data)

        print("wall time:", wall_time)
        print("number of local optima:     ", len(result["local"]))
        print("nominal parameter values:   ", nom_param_vals)
        print("optimal parameter estimates:", opt_param_est.tolist())
        print("ssr (raw):                  ", ssr_raw)        
        print("ssr (fit):                  ", ssr_fit)        
        if self.do_plotting:
            rpt.plot_fit(times, observations, tt, trajectories_raw[1:], labels[1:], self.model_key)
            rpt.plot_fit(times, observations, tt, trajectories_fit[1:], labels[1:], self.model_key)

        self.assertTrue(len(result["local"]) == 3)
        actual = result["global"]["objective_function"]
        expected = 0.021119404945328022
        self.assertAlmostEquals(actual, expected, 12)


if __name__ == "__main__":
    run_slow_tests = True
    suite = unittest.TestSuite()
    suite.addTest(TestExperiment04("test_simulate"))
    suite.addTest(TestExperiment04("test_metric"))
    suite.addTest(TestExperiment04("test_calibrate"))
    if run_slow_tests:
        suite.addTest(TestExperiment04("test_calibrate_global"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
