
import unittest

import copy
import numpy

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
        baseline["intervals"] = [[0.81310699285569032, 1.7939381418621563], [2.0006829540098252, 2.4910985135890753]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCI linear model"
        self.do_test_compute_nonlinear_confidence_intervals( \
            self.do_setup_lin, self.do_experiment_setup_lin, baseline)


    def test_compute_nonlinear_confidence_intervals_nonlin(self):
        baseline = dict(self.baseline)
        baseline["intervals"] = [[0.8671657007822573, 1.5577381993790731], [1.9990400864599849, 2.3057674332509652]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCI nonlinear model"
        self.do_test_compute_nonlinear_confidence_intervals( \
            self.do_setup_nonlin, self.do_experiment_setup_nonlin, baseline)


    def do_test_compute_nonlinear_confidence_region_both(self, setup, config, baseline):
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
        region = ecr.compute_nonlinear_confidence_region_points( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        number_of_points = len(numpy.transpose(region["objective_function"]))
        self.assertEquals(number_of_points, baseline["number_of_points"])

        # do nonlin conf intvs
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
            self.do_setup_lin, self.do_experiment_setup_lin, baseline)


    def test_compute_nonlinear_confidence_region_points_and_intervals_nonlin(self):
        baseline = {}
        baseline["number_of_points"] = 7836
        baseline["intervals"] = [[0.8671657007822573, 1.5577381993790731], [1.9990400864599849, 2.3057674332509652]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR nonlinear model"
        self.do_test_compute_nonlinear_confidence_region_both( \
            self.do_setup_nonlin, self.do_experiment_setup_nonlin, baseline)


    def do_test_compute_linearised_confidence_region_both(self, config, best, baseline):
        intervals = ecr.compute_linearised_confidence_intervals(config, best)
        expected = baseline["intervals"]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(numpy.asarray(intervals).flatten(), expected.flatten())]
        ellipsoid = ecr.compute_linearised_confidence_region_ellipsoid(config, best)
        expected = baseline["ellipsoid"]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip( \
            numpy.asarray(ellipsoid).flatten(), numpy.asarray(expected).flatten())]
        
        if self.do_plotting:
            repl.plot_ellipse_and_box(best['decision_variables'], ellipsoid, intervals, baseline["plotdata"])


    def test_compute_linearised_confidence_region_ellipsoid_and_intervals_lin(self):
        best = {}
        best['objective_function'] = 37.641550819151604
        best['decision_variables'] = [1.30352132, 2.24589073]
        baseline = {}
        baseline["intervals"] = numpy.asarray([[0.81011790765132297, 1.796924732348677], [1.9991890253485634, 2.4925924346514372]])
        baseline["ellipsoid"] = numpy.asarray([[2.40507423e-01, 3.04517007e-10], [3.04517007e-10, 6.01268550e-02]])
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR linear model"
        self.do_test_compute_linearised_confidence_region_both(self.do_experiment_setup_lin(), best, baseline)

        
    def test_compute_linearised_confidence_region_ellipsoid_and_intervals_nonlin(self):
        best = {}
        best['objective_function'] = 37.67831358169179
        best['decision_variables'] = [1.2175145, 2.15319774]
        baseline = {}
        baseline["intervals"] = numpy.asarray([[0.87032574595894485, 1.5647032540410553], [1.9989498251354314, 2.3074456548645683]])
        baseline["ellipsoid"] = numpy.asarray([[1.19200873e-01, -4.59099258e-09], [-4.59099258e-09, 2.35280936e-02]])
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR nonlinear model"
        self.do_test_compute_linearised_confidence_region_both(self.do_experiment_setup_nonlin(), best, baseline)


if __name__ == "__main__":
    unittest.main()