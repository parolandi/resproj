
import unittest

import copy
import numpy

import metrics.ordinary_differential as mod
import models.model_data_utils as mmdu
import engine.confidence_regions as ecr
import results.plot as repl
import setups.ordinary_differential as sod
import setups.setup_data as sesd
import solvers.least_squares as sls
import solvers.monte_carlo_multiple_initial_value as mcmiv
import solvers.solver_data as ssd
import workflows.reporting as wr


class TestOrdinaryDifferential(unittest.TestCase):


    baseline = {}
    baseline["number_of_points"] = 0
    

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
        config["sensitivity_setup"] = None
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
        config["sensitivity_setup"] = None
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
        if self.do_plotting:
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
            repl.plot_scatter(numpy.transpose(points)[0], numpy.transpose(points)[1])


    def test_compute_nonlinear_confidence_region_points_lin(self):
        baseline = dict(self.baseline)
        baseline["number_of_points"] = 7834
        self.do_test_compute_nonlinear_confidence_region_points( \
            self.do_setup_lin, self.do_experiment_setup_lin, baseline)

    
    def test_compute_nonlinear_confidence_region_points_nonlin(self):
        baseline = dict(self.baseline)
        baseline["number_of_points"] = 7841
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
        if self.do_plotting:
            experiment = config()
            wr.plot_tiled_trajectories_at_point(experiment, best_point)
    
        # setup nonlin conf intvs
        model, problem, algorithm_rf = setup()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        
        # do nonlin conf intvs
        actual = ecr.compute_nonlinear_confidence_intervals( \
            model, problem, algorithm_rf, best_point)
        #print(actual)
        self.assertEquals(actual, baseline["intervals"])

        # plot nonlin conf ints
        if self.do_plotting:
            repl.plot_box(actual)


    def test_compute_nonlinear_confidence_intervals_lin(self):
        baseline = dict(self.baseline)
        baseline["intervals"] = [[1.2421237393664939, 1.3649213376271863], [2.2151913416682403, 2.2765901228560925]]
        self.do_test_compute_nonlinear_confidence_intervals( \
            self.do_setup_lin, self.do_experiment_setup_lin, baseline)


    def test_compute_nonlinear_confidence_intervals_nonlin(self):
        baseline = dict(self.baseline)
        baseline["intervals"] = [[1.1742834200072017, 1.2605897448526138], [2.1339948902051442, 2.1723709852890125]]
        self.do_test_compute_nonlinear_confidence_intervals( \
            self.do_setup_nonlin, self.do_experiment_setup_nonlin, baseline)


if __name__ == "__main__":
    unittest.main()