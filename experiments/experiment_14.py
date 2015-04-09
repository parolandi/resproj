
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
        self.do_reduced_mc_sample = True
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
        intervals = ecr.compute_linearised_confidence_intervals(config, best_point)
        expected = baseline["intervals"]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(numpy.asarray(intervals).flatten(), numpy.asarray(expected).flatten())]
        ellipsoid = ecr.compute_linearised_confidence_region_ellipsoid(config, best_point)
        expected = baseline["ellipsoid"]
        diff = baseline["delta"]
        [self.assertAlmostEquals(act, exp, delta=eps) for act, exp, eps in zip( \
            numpy.asarray(ellipsoid).flatten(), numpy.asarray(expected).flatten(), numpy.asarray(diff).flatten())]
        
        if self.do_plotting:
            replco.plot_combinatorial_ellipsoid_projections(best_point['decision_variables'], ellipsoid)        

    
    def do_test_compute_nonlinear_confidence_region_points(self, config, baseline):
        best_point = self.do_regression(config())

        # setup nonlin conf reg
        model, problem, algorithm_rf = self.get_model_problem_algorithm(config())
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 80000
        if self.do_reduced_mc_sample:
            algorithm_mc["number_of_trials"] = 100

        if True:
            self.do_appy_bounds(best_point["decision_variables"], problem)
        logging.info(problem["bounds"])
        
        # do nonlin conf reg
        wall_time0 = time.time()
        actual_intervals, actual_points = ecr.compute_nonlinear_confidence_region_intervals_and_points_extremal( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        wall_time = time.time() - wall_time0
        number_of_points = len(numpy.transpose(actual_points["objective_function"]))
        logging.info(actual_points)
        logging.info(wall_time)
        logging.info(algorithm_mc["number_of_trials"])
        logging.info(number_of_points)
        self.assertEquals(number_of_points, baseline["number_of_points"])
        expected = baseline["intervals"]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip( \
            numpy.asarray(actual_intervals).flatten(), numpy.asarray(expected).flatten())]
        
        # plot nonlin conf reg
        if self.do_plotting:
            replco.plot_combinatorial_region_projections(numpy.transpose(actual_points["decision_variables"]))


    def test_ncr(self):
        baseline = {}
        baseline["number_of_points"] = 80
        baseline["intervals"] = [ \
            [1.8560953554168591e-05, 0.00028858598850377325], \
            [5999621.511495593, 311185069.71460104], \
            [0.00063242352072096094, 0.040354449881673735], \
            [0.0062924327562778317, 62.924327562777854]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model (95%)"
        self.do_test_compute_nonlinear_confidence_region_points(self.do_experiment_setup, baseline)

     
    def test_ncr_low_confidence(self):
        baseline = {}
        baseline["number_of_points"] = 81
        baseline["intervals"] = [ \
            [1.9918149990245181e-05, 0.00027202677048785735], \
            [5999903.1790274335, 6000588.7692325944], \
            [0.00070910862594929702, 0.037986101795423888], \
            [0.0062924327298415237, 62.924327562777854]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model (25%)"
        self.do_test_compute_nonlinear_confidence_region_points(self.do_experiment_setup_with_low_confidence, baseline)

    
    def test_lcr(self):
        baseline = {}
        baseline["intervals"] = [ \
            [4.9423053215497172e-05, 0.00026694444088288676], \
            [-113597360.94805983, 125597359.64413485], \
            [-0.26987827573815093, 0.33646951374979961], \
            [-513.87991160491765, 515.13839815617325]]
        baseline["ellipsoid"] = [ \
            [  6.12718097e-06, -1.09502057e+05,  8.69533106e-04, -2.02686196e+00], \
            [ -1.09502057e+05,  7.40900618e+18,  5.94586975e+08, -8.05367692e+12], \
            [  8.69533106e-04,  5.94586975e+08,  4.76102404e+01, -6.33519915e+04], \
            [ -2.02686196e+00, -8.05367692e+12, -6.33519915e+04,  1.37120687e+08]]
        baseline["delta"] = [ \
            [  0.00000001e-06,  0.00000001e+05,  0.00000001e-04,  0.00000001e+00], \
            [  0.00000001e+05,  0.00000001e+18,  0.00000001e+08,  0.00000001e+12], \
            [  0.00000001e-04,  0.00000001e+08,  0.00000001e+01,  0.00000001e+04], \
            [  0.00000001e+00,  0.00000001e+12,  0.00000001e+04,  0.00000001e+08]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR benchmark model (95%)"
        self.do_test_compute_linearised_confidence_region(self.do_experiment_setup(), baseline)


    def test_lcr_low_confidence(self):
        baseline = {}
        baseline["intervals"] = [ \
            [0.00014082795520386246, 0.00017553953889452146], \
            [-13085083.850529518, 25085082.546604555], \
            [-0.015084203011126875, 0.081675441022775491], \
            [-81.474993833023916, 82.733480384279488]]
        baseline["ellipsoid"] = [ \
            [  1.15263027e-06, -2.05992587e+04,  1.63574438e-04, -3.81288306e-01], \
            [ -2.05992587e+04,  1.39376409e+18,  1.11852245e+08, -1.51503797e+12], \
            [  1.63574438e-04,  1.11852245e+08,  8.95632179e+00, -1.19176214e+04], \
            [ -3.81288306e-01, -1.51503797e+12, -1.19176214e+04,  2.57948078e+07]]
        baseline["delta"] = [ \
            [  0.00000001e-06,  0.00000001e+04,  0.00000001e-04,  0.00000001e-01], \
            [  0.00000001e+04,  0.00000001e+18,  0.00000001e+08,  0.00000001e+12], \
            [  0.00000001e-04,  0.00000001e+08,  0.00000001e+00,  0.00000001e+04], \
            [  0.00000001e-01,  0.00000001e+12,  0.00000001e+04,  0.00000001e+07]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR benchmark model (25%)"
        self.do_test_compute_linearised_confidence_region(self.do_experiment_setup_with_low_confidence(), baseline)


if __name__ == "__main__":
    unittest.main()
