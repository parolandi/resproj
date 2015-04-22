
import unittest

import copy
import logging
import numpy

import common.diagnostics as codi
import metrics.ordinary_differential as mod
import models.model_data_utils as mmdu
import engine.confidence_regions as ecr
import results.plot as repl
import results.plot_data as replda
import setups.ordinary_differential as sod
import setups.setup_data as sesd
import solvers.least_squares as sls
import solvers.local_sensitivities as solose
import solvers.monte_carlo_multiple_initial_value as mcmiv
import solvers.solver_data as ssd
import workflows.reporting as wr


class TestOrdinaryDifferential(unittest.TestCase):


    baseline = {}
    baseline["number_of_points"] = 0
    baseline["intervals"] = []
    

    def __init__(self, *args, **kwargs):
        super(TestOrdinaryDifferential, self).__init__(*args, **kwargs)
        self.do_plotting = False
        logging.basicConfig(filename=codi.get_name_logging_file(), level=codi.get_logging_level())

    
    def do_setup_lin(self):
        config = self.do_experiment_setup_lin()
        algorithm = config["algorithm_setup"]()
        data = config["data_setup"]()
        model = config["model_setup"]()
        problem = config["problem_setup"](model, data["calib"])
        return model, problem, algorithm

    
    def do_setup_nonlin(self):
        config = self.do_experiment_setup_nonlin()
        algorithm = config["algorithm_setup"]()
        data = config["data_setup"]()
        model = config["model_setup"]()
        problem = config["problem_setup"](model, data["calib"])
        return model, problem, algorithm

    
    def do_setup_nonlin_in_params(self):
        config = self.do_experiment_setup_nonlin_in_params()
        algorithm = config["algorithm_setup"]()
        data = config["data_setup"]()
        model = config["model_setup"]()
        problem = config["problem_setup"](model, data["calib"])
        return model, problem, algorithm

    
    def do_setup_nonlin_in_params_twice(self):
        config = self.do_experiment_setup_nonlin_in_params_twice()
        algorithm = config["algorithm_setup"]()
        data = config["data_setup"]()
        model = config["model_setup"]()
        problem = config["problem_setup"](model, data["calib"])
        return model, problem, algorithm

    
    def do_experiment_setup_nonlin(self):
        config = copy.deepcopy(sesd.experiment_setup)
        config["algorithm_setup"] = self.do_algorithm_setup
        config["data_setup"] = sod.do_data_setup_nonlin_spliced_111111_without_covariance
        config["model_setup"] = sod.do_model_setup_nonlin
        config["problem_setup"] = sod.do_problem_setup_without_covariance
        config["protocol_setup"] = None
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        config["sensitivity_setup"] = solose.compute_timecourse_trajectories_and_sensitivities
        return config

    
    def do_experiment_setup_lin(self):
        config = copy.deepcopy(sesd.experiment_setup)
        config["algorithm_setup"] = self.do_algorithm_setup
        config["data_setup"] = sod.do_baseline_data_setup_spliced_111111_without_covariance
        config["model_setup"] = sod.do_model_setup
        config["problem_setup"] = sod.do_problem_setup_without_covariance
        config["protocol_setup"] = None
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        config["sensitivity_setup"] = solose.compute_timecourse_trajectories_and_sensitivities
        return config

    
    def do_experiment_setup_nonlin_in_params(self):
        config = copy.deepcopy(sesd.experiment_setup)
        config["algorithm_setup"] = self.do_algorithm_setup
        config["data_setup"] = sod.do_data_setup_nonlin_in_params_spliced_111111_without_covariance
        config["model_setup"] = sod.do_model_setup_nonlin_in_params
        config["problem_setup"] = sod.do_problem_setup_without_covariance
        config["protocol_setup"] = None
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        config["sensitivity_setup"] = solose.compute_timecourse_trajectories_and_sensitivities
        return config

    
    def do_experiment_setup_nonlin_in_params_twice(self):
        config = self.do_experiment_setup_nonlin_in_params()
        config["problem_setup"] = sod.do_problem_setup_without_covariance_twice
        return config
    
    
    def do_algorithm_setup(self):
        algorithm = copy.deepcopy(ssd.algorithm_structure)
        algorithm["initial_guesses"] = numpy.asarray([1.0])
        algorithm["method"] = 'SLSQP'
        return algorithm


    def do_test_compute_nonlinear_confidence_region_points(self, setup, config, baseline):
        # setup regression
        model, problem, _ = setup()
        algorithm = dict(ssd.algorithm_structure)
        algorithm["initial_guesses"] = problem["parameters"]
        algorithm["method"] = 'SLSQP'

        # do regression        
        dvs = sls.solve(model, problem, algorithm)
        mmdu.apply_values_to_parameters(dvs.x, model, problem)
        obj = mod.sum_squared_residuals_st(None, None, model, problem)
        best_point = {}
        best_point["decision_variables"] = dvs.x
        best_point["objective_function"] = obj
        
        # plot regression
        if False:
            experiment = config()
            wr.plot_tiled_trajectories_at_point(experiment, best_point)
    
        # setup nonlin conf reg
        model, problem, algorithm_rf = setup()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        
        # do nonlin conf reg
        actual = ecr.compute_nonlinear_confidence_region_points( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        number_of_points = len(numpy.transpose(actual["objective_function"]))
        self.assertEquals(number_of_points, baseline["number_of_points"])

        # plot nonlin conf reg
        if self.do_plotting:
            points = numpy.asarray(actual["decision_variables"])
            repl.plot_scatter(numpy.transpose(points)[0], numpy.transpose(points)[1], baseline["plotdata"])


    def test_compute_nonlinear_confidence_region_points_lin(self):
        baseline = dict(self.baseline)
        baseline["number_of_points"] = 7834
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR linear model"
        self.do_test_compute_nonlinear_confidence_region_points( \
            self.do_setup_lin, self.do_experiment_setup_lin, baseline)

    
    def test_compute_nonlinear_confidence_region_points_nonlin(self):
        baseline = dict(self.baseline)
        baseline["number_of_points"] = 7836
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR nonlinear model"
        self.do_test_compute_nonlinear_confidence_region_points( \
            self.do_setup_nonlin, self.do_experiment_setup_nonlin, baseline)


    def do_test_compute_nonlinear_confidence_intervals(self, setup, config, baseline):
        # setup regression
        model, problem, _ = setup()
        algorithm = dict(ssd.algorithm_structure)
        algorithm["initial_guesses"] = problem["parameters"]
        algorithm["method"] = 'SLSQP'

        # do regression        
        dvs = sls.solve(model, problem, algorithm)
        mmdu.apply_values_to_parameters(dvs.x, model, problem)
        obj = mod.sum_squared_residuals_st(None, None, model, problem)
        best_point = {}
        best_point["decision_variables"] = dvs.x
        best_point["objective_function"] = obj
        
        # plot regression
        if False:
            experiment = config()
            wr.plot_tiled_trajectories_at_point(experiment, best_point)
    
        # setup nonlin conf intvs
        model, problem, algorithm_rf = setup()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        
        # do nonlin conf intvs
        actual = ecr.compute_nonlinear_confidence_intervals( \
            model, problem, algorithm_rf, best_point)
        self.assertEquals(actual, baseline["intervals"])

        # plot nonlin conf ints
        if self.do_plotting:
            repl.plot_box(actual, baseline["plotdata"])


    def test_compute_nonlinear_confidence_intervals_lin(self):
        baseline = dict(self.baseline)
        baseline["intervals"] = [[0.81310699293708133, 1.7939381418597145], [2.0006829540095556, 2.4910985135866737]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCI linear model"
        self.do_test_compute_nonlinear_confidence_intervals( \
            self.do_setup_lin, self.do_experiment_setup_lin, baseline)


    def test_compute_nonlinear_confidence_intervals_nonlin(self):
        baseline = dict(self.baseline)
        baseline["intervals"] = [[0.86716570038943908, 1.5577383074233793], [1.9990400864063649, 2.3057674333232421]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCI nonlinear model"
        self.do_test_compute_nonlinear_confidence_intervals( \
            self.do_setup_nonlin, self.do_experiment_setup_nonlin, baseline)


    def do_test_compute_nonlinear_confidence_region_both(self, setup, config, baseline, do_extremal):
        # setup regression
        model, problem, _ = setup()
        algorithm = dict(ssd.algorithm_structure)
        algorithm["initial_guesses"] = problem["parameters"]
        algorithm["method"] = 'SLSQP'

        # do regression        
        dvs = sls.solve(model, problem, algorithm)
        mmdu.apply_values_to_parameters(dvs.x, model, problem)
        obj = mod.sum_squared_residuals(None, model, problem)
        best_point = {}
        best_point["decision_variables"] = dvs.x
        best_point["objective_function"] = obj
        # plot regression
        if False:
            experiment = config()
            wr.plot_tiled_trajectories_at_point(experiment, best_point)
    
        # setup nonlin conf reg
        model, problem, algorithm_rf = setup()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        
        # do nonlin conf reg
        if do_extremal:
            region = ecr.compute_nonlinear_confidence_region_points_extremal( \
                model, problem, algorithm_rf, algorithm_mc, best_point)
        else:
            region = ecr.compute_nonlinear_confidence_region_points( \
                model, problem, algorithm_rf, algorithm_mc, best_point)
        number_of_points = len(numpy.transpose(region["objective_function"]))
        self.assertEquals(number_of_points, baseline["number_of_points"])

        # do nonlin conf intvs
        if do_extremal:
            intervals, _ = ecr.compute_nonlinear_confidence_intervals_extremal( \
                model, problem, algorithm_rf, best_point)
        else:
            intervals = ecr.compute_nonlinear_confidence_intervals( \
                model, problem, algorithm_rf, best_point)
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip( \
            numpy.asarray(intervals).flatten(), numpy.asarray(baseline["intervals"]).flatten())]

        if self.do_plotting:
            points = numpy.asarray(region["decision_variables"])
            repl.plot_scatter_and_box( \
                numpy.transpose(points)[0], numpy.transpose(points)[1], intervals, baseline["plotdata"])


    def test_compute_nonlinear_confidence_region_points_and_intervals_lin(self):
        baseline = {}
        baseline["number_of_points"] = 7834
        baseline["intervals"] = [[0.81310699285569032, 1.7939381418621563], [2.0006829540098252, 2.4910985135890753]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR linear model"
        self.do_test_compute_nonlinear_confidence_region_both( \
            self.do_setup_lin, self.do_experiment_setup_lin, baseline, False)


    def test_compute_nonlinear_confidence_region_points_and_intervals_nonlin_in_params(self):
        baseline = {}
        baseline["number_of_points"] = 1926
        baseline["intervals"] = [[0.81310695394950572, 1.7939381493831716], [1.2251143177940427, 2.7889286158913245]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR nl-in-params model"
        self.do_test_compute_nonlinear_confidence_region_both( \
            self.do_setup_nonlin_in_params, \
            self.do_experiment_setup_nonlin_in_params, \
            baseline, True)

    
    def test_compute_nonlinear_confidence_region_points_and_intervals_nonlin(self):
        baseline = {}
        baseline["number_of_points"] = 7836
        baseline["intervals"] = [[0.86716570038943908, 1.5577383074233793], [1.9990400864063649, 2.3057674333232421]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR nonlinear model"
        self.do_test_compute_nonlinear_confidence_region_both( \
            self.do_setup_nonlin, self.do_experiment_setup_nonlin, baseline, False)


    def do_test_compute_linearised_confidence_region_both(self, config, dummy, baseline):
        # setup regression
        model = config["model_setup"]()
        data = config["data_setup"]()
        problem = config["problem_setup"](model, data["calib"])
        algorithm = dict(ssd.algorithm_structure)
        algorithm["initial_guesses"] = problem["parameters"]
        algorithm["method"] = 'SLSQP'

        # do regression        
        dvs = sls.solve(model, problem, algorithm)
        mmdu.apply_values_to_parameters(dvs.x, model, problem)
        obj = mod.sum_squared_residuals_st(None, None, model, problem)
        best_point = {}
        best_point["decision_variables"] = dvs.x
        best_point["objective_function"] = obj
        # plot regression
        if False:
            experiment = config()
            wr.plot_tiled_trajectories_at_point(experiment, best_point)
    
        # setup lin conf reg
        intervals = ecr.compute_linearised_confidence_intervals(config, best_point)
        expected = baseline["intervals"]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(numpy.asarray(intervals).flatten(), expected.flatten())]
        ellipsoid = ecr.compute_linearised_confidence_region_ellipsoid(config, best_point)
        expected = baseline["ellipsoid"]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip( \
            numpy.asarray(ellipsoid).flatten(), numpy.asarray(expected).flatten())]
        
        if self.do_plotting:
            repl.plot_ellipse_and_box(best_point['decision_variables'], ellipsoid, intervals, baseline["plotdata"])


    def test_compute_linearised_confidence_region_ellipsoid_and_intervals_lin(self):
        best = {}
        best['objective_function'] = 37.641550819151604
        best['decision_variables'] = [1.30352132, 2.24589073]
        baseline = {}
        baseline["intervals"] = numpy.asarray( \
            [[0.81011933848394491, 1.7969261581836407], [1.9991892307205215, 2.4925926400082798]])
        baseline["ellipsoid"] = numpy.asarray( \
            [[2.40507421e-01, 5.11875837e-11], [5.11875837e-11, 6.01268550e-02]])
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR linear model"
        self.do_test_compute_linearised_confidence_region_both(self.do_experiment_setup_lin(), best, baseline)

    
    def test_compute_linearised_confidence_region_ellipsoid_and_intervals_nonlin_in_params(self):
        best = {}
        best['objective_function'] = 37.641550819151604
        best['decision_variables'] = [1.30352132, 2.24589073]
        baseline = {}
        baseline["intervals"] = numpy.asarray( \
            [[0.81010420905522618, 1.7969110309175582], [1.043879207104472, 2.4020409552085669]])
        baseline["ellipsoid"] = numpy.asarray( \
            [[0.24050742, -0.3178997 ], [-0.3178997, 0.45558266]])
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR nl-in-params model"
        self.do_test_compute_linearised_confidence_region_both(self.do_experiment_setup_nonlin_in_params(), best, baseline)

    
    def test_compute_nonlinear_confidence_region_points_and_intervals_nonlin_in_params_twice(self):
        baseline = {}
        baseline["number_of_points"] = 2284
        baseline["intervals"] = [[0.96398973047805259, 1.6430554105601161], [1.3483585398194338, 2.2014435078083596]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR nl-in-params model (twice)"
        self.do_test_compute_nonlinear_confidence_region_both( \
            self.do_setup_nonlin_in_params_twice, \
            self.do_experiment_setup_nonlin_in_params_twice, \
            baseline, True)
    
    
    def test_compute_linearised_confidence_region_ellipsoid_and_intervals_nonlin(self):
        best = {}
        best['objective_function'] = 37.67831358169179
        best['decision_variables'] = [1.2175145, 2.15319774]
        baseline = {}
        baseline["intervals"] = numpy.asarray( \
            [[0.87032901438999888, 1.56470648184485], [1.9989529309168752, 2.3074487011812739]])
        baseline["ellipsoid"] = numpy.asarray( \
            [[1.19200859e-01, 1.73880317e-08], [1.73880317e-08, 2.35280846e-02]])
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR nonlinear model"
        self.do_test_compute_linearised_confidence_region_both(self.do_experiment_setup_nonlin(), best, baseline)


if __name__ == "__main__":
    unittest.main()