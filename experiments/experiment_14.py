
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy
import time

import common.diagnostics as codi
import metrics.ordinary_differential as mod
import models.model_data_utils as mmdu
import engine.confidence_regions as ecr
import results.plot_combinatorial as replco
import results.plot_data as replda
import solvers.least_squares as sls
import solvers.monte_carlo_multiple_initial_value as mcmiv
import workflows.reporting as wr


class TestExperiment14(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment14, self).__init__(*args, **kwargs)
        self.do_plotting = False
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())

    
    def do_experiment_setup(self):
        config = sekrbi.do_experiment_setup()
        config["algorithm_setup"] = sekrbi.do_algorithm_setup_using_slsqp_with_positivity
        return config


    def do_experiment_setup_with_low_confidence(self):
        config = self.do_experiment_setup()
        config["problem_setup"] = sekrbi.do_problem_setup_with_covariance_2_and_low_confidence
        return config

    
    def get_model_problem_algorithm(self, config):
        algorithm = config["algorithm_setup"](None)
        data = config["data_setup"]()
        model = config["model_setup"]()
        problem = config["problem_setup"](model, data["calib"])
        return model, problem, algorithm

    
    def do_appy_bounds(self, nominal, problem):
        lf = 1E-2
        uf = 1E+2
        problem["bounds"] = [ \
            (nominal[0]*lf,nominal[0]*uf), \
            (nominal[1]*lf,nominal[1]*uf), \
            (nominal[2]*lf,nominal[2]*uf), \
            (nominal[3]*lf,nominal[3]*uf)]
        
    
    def do_apply_bound_experimental(self, problem):
        bounds = [[1.8560954071217014e-05, 0.00028822938131456123], [5999964.775229332, 5999999.3480375186], [0.0033295619005827282, 0.040367992439463547], [0.62924327562778315, 6.2924327562778313]]
        fc = 5
        problem["bounds"][0] = [bounds[0][0]/fc,bounds[0][1]*fc]
        problem["bounds"][1] = [bounds[1][0]/fc,bounds[1][1]*fc]
        problem["bounds"][2] = [bounds[2][0]/fc,bounds[2][1]*fc]
        problem["bounds"][3] = [bounds[3][0]/fc,bounds[3][1]*fc]


    def do_regression(self, config):
        # setup regression
        model, problem, algorithm = self.get_model_problem_algorithm(config)

        # do regression        
        dvs = sls.solve(model, problem, algorithm)
        mmdu.apply_values_to_parameters(dvs.x, model, problem)
        obj = mod.sum_squared_residuals_st(None, None, model, problem)
        best_point = {}
        best_point["decision_variables"] = dvs.x
        best_point["objective_function"] = obj
        logging.info(best_point)
        # plot regression
        if False:
            experiment = config()
            wr.plot_tiled_trajectories_at_point(experiment, best_point)
        return best_point


    def do_test_compute_linearised_confidence_region(self, config, baseline):
        best_point = self.do_regression(config)
        
        # setup lin conf reg
        _ = ecr.compute_linearised_confidence_intervals(config, best_point)
        #expected = baseline["intervals"]
        #[self.assertAlmostEquals(act, exp, 8) for act, exp in zip(numpy.asarray(intervals).flatten(), expected.flatten())]
        ellipsoid = ecr.compute_linearised_confidence_region_ellipsoid(config, best_point)
        #expected = baseline["ellipsoid"]
        #[self.assertAlmostEquals(act, exp, 8) for act, exp in zip( \
        #    numpy.asarray(ellipsoid).flatten(), numpy.asarray(expected).flatten())]
        
        if True:
            replco.plot_combinatorial_ellipsoid_projections(best_point['decision_variables'], ellipsoid)        

    
    def do_test_compute_nonlinear_confidence_region_points(self, config, baseline):
        best_point = self.do_regression(config())

        # setup nonlin conf reg
        model, problem, algorithm_rf = self.get_model_problem_algorithm(config())
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 80000

        if True:
            self.do_appy_bounds(best_point["decision_variables"], problem)
        logging.info(problem["bounds"])
        
        # do nonlin conf reg
        wall_time0 = time.time()
        actual = ecr.compute_nonlinear_confidence_region_points_extremal( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        wall_time = time.time() - wall_time0
        number_of_points = len(numpy.transpose(actual["objective_function"]))
        logging.info(actual)
        logging.info(wall_time)
        logging.info(algorithm_mc["number_of_trials"])
        logging.info(number_of_points)
        #self.assertEquals(number_of_points, baseline["number_of_points"])
        
        # plot nonlin conf reg
        if self.do_plotting:
            replco.plot_combinatorial_region_projections(numpy.transpose(actual["decision_variables"]))


    def test_ncr(self):
        baseline = {}
        baseline["number_of_points"] = 7834
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model"
        self.do_test_compute_nonlinear_confidence_region_points(self.do_experiment_setup, None)
        self.assertFalse(True)

     
    def test_lcr(self):
        baseline = {}
        baseline["number_of_points"] = -1
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR benchmark model"
        self.do_test_compute_linearised_confidence_region(self.do_experiment_setup(), None)
        self.assertFalse(True)


    def test_lcr_low_confidence(self):
        baseline = {}
        baseline["number_of_points"] = -1
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR benchmark model"
        self.do_test_compute_linearised_confidence_region(self.do_experiment_setup_with_low_confidence(), None)
        self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()
