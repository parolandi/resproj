
import unittest
import engine.confidence_regions as testme

import copy
import numpy
import scipy.stats

import results.plot as repl
import setups.ordinary_differential as sod
import setups.setup_data as seseda
import solvers.local_sensitivities as solose
import solvers.monte_carlo_multiple_initial_value as mcmiv
import solvers.solver_data as ssd

import metrics.ordinary_differential as meordi


class TestConfidenceRegions(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestConfidenceRegions, self).__init__(*args, **kwargs)
        self.do_plotting = False

    
    def do_experiment_setup_lin(self):
        config = copy.deepcopy(seseda.experiment_setup)
        config["algorithm_setup"] = self.do_algorithm_setup
        config["data_setup"] = sod.do_baseline_data_setup_spliced_111111_without_covariance
        config["model_setup"] = sod.do_model_setup
        config["problem_setup"] = sod.do_problem_setup_without_covariance
        config["protocol_setup"] = None
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        config["sensitivity_setup"] = solose.compute_timecourse_trajectories_and_sensitivities
        return config

    
    def do_setup_lin(self):
        algorithm = self.do_algorithm_setup()
        data = sod.do_baseline_data_setup_spliced_111111_without_covariance()
        model = sod.do_model_setup_lin()
        problem = sod.do_problem_setup_without_covariance(model, data["calib"])
        problem["confidence_region"]["ssr"] = 43
        return model, problem, algorithm


    def do_setup_nonlin(self):
        algorithm = self.do_algorithm_setup()
        data = sod.do_data_setup_nonlin_spliced_111111_without_covariance()
        model = sod.do_model_setup_nonlin()
        problem = sod.do_problem_setup_without_covariance(model, data["calib"])
        problem["confidence_region"]["ssr"] = 43
        return model, problem, algorithm

    
    def do_setup_nonlin_in_params(self):
        algorithm = self.do_algorithm_setup()
        data = sod.do_data_setup_nonlin_in_params_spliced_111111_without_covariance()
        model = sod.do_model_setup_nonlin_in_params()
        problem = sod.do_problem_setup_without_covariance(model, data["calib"])
        problem["confidence_region"]["ssr"] = 43
        return model, problem, algorithm

    
    def do_algorithm_setup(self):
        algorithm = copy.deepcopy(ssd.algorithm_structure)
        algorithm["initial_guesses"] = numpy.asarray([1.0])
        algorithm["method"] = 'SLSQP'
        return algorithm
        

    def test_compute_f_constraint(self):
        no_meas = 20
        no_params = 2
        alpha = 0.01
        ssr = scipy.stats.chi2.stats(no_meas-no_params, moments='m')
        est_var = ssr / (no_meas-no_params)
        ssr_threshold = testme.compute_f_constraint(ssr, numpy.ones(no_meas), no_params, 1-alpha)
        self.assertAlmostEquals(ssr + est_var * no_params * scipy.stats.f.isf(alpha, no_params, no_meas - no_params), ssr_threshold, 8)
    
    
    def test_compute_nonlinear_confidence_interval_lin(self):
        model, problem, algorithm = self.do_setup_lin()
        actual = testme.compute_nonlinear_confidence_interval(model, problem, algorithm, 0)
        expected = [1.01338741, 1.59365765]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]


    def test_compute_nonlinear_confidence_interval_nonlin_in_params(self):
        model, problem, algorithm = self.do_setup_nonlin_in_params()
        actual = testme.compute_nonlinear_confidence_interval(model, problem, algorithm, 0)
        expected = [1.0017616818394601, 1.2653734258285729]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]

    
    def test_compute_nonlinear_confidence_hyperrectangle_lin(self):
        model, problem, algorithm = self.do_setup_lin()
        actual = numpy.asarray(testme.compute_nonlinear_confidence_hyperrectangle(model, problem, algorithm))
        expected = numpy.asarray([[1.01338741, 1.59365765], [2.0040739383273261, 2.4877075291690458]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual.flatten(), expected.flatten())]


    def test_empihbnci_lin(self):
        model, problem, _ = self.do_setup_lin()
        algorithm = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(1.01338741, 1.59365765), (2.00000001, 2.49178146)]
        result = testme.evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals( \
            model, problem, algorithm)
        actual = result["objective_function"]
        expected = [ 38.14628465, 41.32395438, 39.65061399, 40.98962304, 39.13358795,  39.49045378, 40.72301099, 38.8659546,  39.339134,   38.4672953 ]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]
        # TODO should also test decision variables

    
    def test_filter_nonlinear_confidence_region_points_lin(self):
        model, problem, _ = self.do_setup_lin()
        algorithm = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(1.01338741, 1.59365765), (2.00000001, 2.49178146)]
        prelim = testme.evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals( \
            model, problem, algorithm)
        cutoff = 38.47
        result = testme.filter_nonlinear_confidence_region_points(prelim, cutoff)
        self.assertTrue(len(result["objective_function"]) == 2)
        # TODO should also test individual values


    def test_compute_nonlinear_confidence_region_points_lin(self):
        best_point = {}
        best_point["decision_variables"] = [ 1.30352132,  2.24589073]
        best_point["objective_function"] = 37.641550819151604
        
        model, problem, algorithm_rf = self.do_setup_lin()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        actual = testme.compute_nonlinear_confidence_region_points( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        self.assertEquals(len(actual["objective_function"]), 7834)

        if self.do_plotting:
            points = numpy.asarray(actual["decision_variables"])
            repl.plot_scatter(numpy.transpose(points)[0], numpy.transpose(points)[1], None)


    def test_compute_nonlinear_confidence_region_points_nonlin(self):
        best_point = {}
        best_point["decision_variables"] = [ 1.2175145 ,  2.15319774]
        best_point["objective_function"] = 37.67831358169179
        
        model, problem, algorithm_rf = self.do_setup_nonlin()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        actual = testme.compute_nonlinear_confidence_region_points( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        self.assertEquals(len(actual["objective_function"]), 7836)

        if self.do_plotting:
            plot_data = {}
            plot_data["window_title"] = "NCR nonlinear model"
            points = numpy.asarray(actual["decision_variables"])
            repl.plot_scatter(numpy.transpose(points)[0], numpy.transpose(points)[1], plot_data)


    def test_compute_linearised_confidence_region_intervals_lin(self):
        config = self.do_experiment_setup_lin()
        best = {}
        best['objective_function'] = 37.641550819151604
        best['decision_variables'] = [1.30352132, 2.24589073]
        intervals = numpy.asarray(testme.compute_linearised_confidence_intervals(config, best))
        expected = numpy.asarray(numpy.asarray([[0.81011790765132297, 1.796924732348677], [1.9991890253485634, 2.4925924346514372]]))
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(intervals.flatten(), expected.flatten())]
        
        if self.do_plotting:
            plot_data = {}
            plot_data["window_title"] = "LCR linear model"
            repl.plot_box(intervals, plot_data)


    def test_compute_linearised_confidence_region_ellipsoid_lin(self):
        config = self.do_experiment_setup_lin()
        best = {}
        best['objective_function'] = 37.641550819151604
        best['decision_variables'] = [1.30352132, 2.24589073]
        ellipsoid = numpy.asarray(testme.compute_linearised_confidence_region_ellipsoid(config, best))
        expected = numpy.asarray([[2.40507423e-01, 3.04517007e-10], [3.04517007e-10, 6.01268550e-02]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(ellipsoid.flatten(), expected.flatten())]
        
        if self.do_plotting:
            plot_data = {}
            plot_data["window_title"] = "LCR linear model"
            repl.plot_ellipse(best['decision_variables'], ellipsoid, plot_data)

    '''---------------------------------------------------------------------'''
    
    # mock
    def do_confidence_region_performance_measure(self, dummy1, dummy2, model, problem):
        param = numpy.asarray(problem["parameters"])
        measure = numpy.dot(param, param)
        return measure
    
    
    def test_likelihood_constraint(self):
        ssr0 = 10
        model = {}
        model["parameters"] = [1, 2]
        problem = {}
        problem["parameters"] = [3, 4]
        problem["parameter_indices"] = [0, 1]
        problem["confidence_region"] = {}
        problem["confidence_region"]["performance_measure"] = self.do_confidence_region_performance_measure
        actual = testme.likelihood_constraint([0, 2], model, problem, ssr0)
        expected = 10-(0**2+2**2)
        self.assertEquals(actual, expected)
    

    def test_form_upper_constraints(self):
        ssr0 = 10
        model = {}
        model["parameters"] = [1, 2]
        problem = {}
        problem["parameters"] = [3, 4]
        problem["parameter_indices"] = [0, 1]
        problem["confidence_region"] = {}
        problem["confidence_region"]["ssr"] = ssr0
        problem["confidence_region"]["performance_measure"] = self.do_confidence_region_performance_measure
        constraints = testme.form_upper_constraints(model, problem)
        actual = constraints[0]['fun']([0, 2], *constraints[0]['args'])
        expected = 10-(0**2+2**2)
        self.assertEquals(actual, expected)
        actual = constraints[1]['fun']([0, 2], *constraints[1]['args'])
        expected = 0-3
        self.assertEquals(actual, expected)
        actual = constraints[2]['fun']([0, 2], *constraints[2]['args'])
        expected = 2-4
        self.assertEquals(actual, expected)
        

    # TODO: these should be consistent!
    def test_compute_nonlinear_confidence_hyperrectangle_extremal_lin(self):
        model, problem, algorithm = self.do_setup_lin()
        algorithm["initial_guesses"] = numpy.asarray([1.0, 2.0])
        problem["confidence_region"]["performance_measure"] = meordi.sum_squared_residuals_st
        problem["parameters"] = [(1.01338741+1.59365765)/2, (2.0040739383273261+2.4877075291690458)/2]
        algorithm["initial_guesses"] = problem["parameters"]
        actual = numpy.asarray(testme.compute_nonlinear_confidence_hyperrectangle_extremal(model, problem, algorithm))
        expected = numpy.asarray( \
            [[0.7325344709901066, 1.8745106620257141], [1.9603966924184313, 2.531384774085117]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual.flatten(), expected.flatten())]


    def test_compute_nonlinear_confidence_hyperrectangle_extremal_nonlin_in_params(self):
        model, problem, algorithm = self.do_setup_nonlin_in_params()
        algorithm["initial_guesses"] = numpy.asarray([1.0, 2.0])
        problem["confidence_region"]["performance_measure"] = meordi.sum_squared_residuals_st
        problem["parameters"] = [(1.0017616818394601+1.2653734258285729)/2, (2.0040739383273261+2.4877075291690458)/2]
        algorithm["initial_guesses"] = problem["parameters"]
        actual = numpy.asarray(testme.compute_nonlinear_confidence_hyperrectangle_extremal(model, problem, algorithm))
        expected = numpy.asarray( \
            [[0.73253445143590945, 1.8745106623661127], [1.1668645358421914, 3.0971745938850002]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual.flatten(), expected.flatten())]


    def test_compute_nonlinear_confidence_hyperrectangle_extremal_nonlin_in_params_w_bounds_mod(self):
        model, problem, algorithm = self.do_setup_nonlin_in_params()
        algorithm["initial_guesses"] = numpy.asarray([1.0, 2.0])
        problem["confidence_region"]["performance_measure"] = meordi.sum_squared_residuals_st
        problem["parameters"] = [(1.0017616818394601+1.2653734258285729)/2, (2.0040739383273261+2.4877075291690458)/2]
        problem["bounds"] = [(0,10), (0,10)]
        algorithm["initial_guesses"] = problem["parameters"]
        actual = numpy.asarray(testme.compute_nonlinear_confidence_hyperrectangle_extremal(model, problem, algorithm))
        expected = numpy.asarray( \
            [[0.73253445143590945, 1.8745106725484639], [1.1668645358421914, 3.0971746922364414]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual.flatten(), expected.flatten())]


    def test_compute_nonlinear_confidence_hyperrectangle_extremal_lin_pseudo_bounded(self):
        model, problem, algorithm = self.do_setup_lin()
        algorithm["initial_guesses"] = numpy.asarray([1.0, 2.0])
        problem["confidence_region"]["performance_measure"] = meordi.sum_squared_residuals_st
        point = [(1.01338741+1.59365765)/2, (2.0040739383273261+2.4877075291690458)/2]
        problem["parameters"] = point
        algorithm["initial_guesses"] = problem["parameters"]
        bounded = [(point[0]-0.01,point[0]+0.01), (point[1]-0.01,point[1]+0.01)]
        problem["bounds"] = copy.deepcopy(bounded)
        actual = numpy.asarray(testme.compute_nonlinear_confidence_hyperrectangle_extremal(model, problem, algorithm))
        expected = numpy.asarray(bounded)
        [self.assertAlmostEquals(act, exp, 12) for act, exp in zip(actual.flatten(), expected.flatten())]


if __name__ == "__main__":
    unittest.main()
