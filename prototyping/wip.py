
import unittest
import solvers.initial_value

import copy
import numpy
import time
import logging

import models.model_data as momoda
#import setups.setup_data_utils as sesedaut
#import workflows.protocols as wopr
import setups.kremlingetal_bioreactor as sekrbi
import workflows.experiments as woex
import workflows.reporting as wore
import results.plot_combinatorial as replco
import engine.confidence_regions as ecr
import solvers.monte_carlo_multiple_initial_value as mcmiv
import results.plot_data as replda

import common.diagnostics as codi
import metrics.ordinary_differential as mod
import models.model_data_utils as mmdu
import engine.confidence_regions as ecr
import results.plot_combinatorial as replco
import results.plot_data as replda
import solvers.least_squares as sls
import solvers.monte_carlo_multiple_initial_value as mcmiv
import workflows.reporting as wr


# states, time, parameters, inputs
def linear_mock(x, t, p, u):
    return p[0] * u[0]


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    dx_dt = numpy.multiply(p, u)
    return dx_dt


# TODO: test with subset of "dofs"
class TestWip(unittest.TestCase):


    def do_setup(self):
        problem_instance = dict(momoda.problem_structure)
        problem_instance["initial_conditions"] = [0.0]
        problem_instance["parameters"] = [1.0]
        problem_instance["inputs"] = [1.0]
        
        model_instance = dict(momoda.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        return model_instance, problem_instance


    def do_setup_2p2s(self):
        problem_instance = dict(momoda.problem_structure)
        problem_instance["initial_conditions"] = [0.0, 1.0]
        problem_instance["parameters"] = [1.0, 0.5]
        problem_instance["inputs"] = [1.0, 2.0]
        
        model_instance = dict(momoda.model_structure)
        model_instance["parameters"] = copy.deepcopy(problem_instance["parameters"])
        model_instance["inputs"] = copy.deepcopy(problem_instance["inputs"])
        model_instance["states"] = copy.deepcopy(problem_instance["initial_conditions"])
        model_instance["time"] = 0.0

        return model_instance, problem_instance

    
    def do_setup_2p2s_with_forcing_inputs(self):
        model, problem = self.do_setup_2p2s()
        forcing_inputs = copy.deepcopy(momoda.forcing_function_profile)
        forcing_inputs["continuous_time_intervals"] = [0,0.5,0.9]
        forcing_inputs["piecewise_constant_inputs"] = [numpy.asarray([1,2]), numpy.asarray([2,2])]
        problem["forcing_inputs"] = forcing_inputs
        problem["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=False)
        return model, problem


    def do_test_compute_nonlinear_confidence_region_points(self, config, baseline):
        best_point = self.do_regression(config())

        # setup nonlin conf reg
        model, problem, algorithm_rf = self.get_model_problem_algorithm(config())
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 120000*4
        if True:
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
        #self.assertEquals(number_of_points, baseline["number_of_points"])
        expected = baseline["intervals"]
        #[self.assertAlmostEquals(act, exp, 8) for act, exp in zip( \
        #    numpy.asarray(actual_intervals).flatten(), numpy.asarray(expected).flatten())]
        
        # plot nonlin conf reg
        if True:
            replco.plot_combinatorial_region_projections(numpy.transpose(actual_points["decision_variables"]))


    def do_appy_bounds(self, nominal, problem):
        lf = 1E-2
        uf = 1E+2
        problem["bounds"] = [ \
            (nominal[0]*lf,nominal[0]*uf), \
            (nominal[1]*lf,nominal[1]*uf), \
            (nominal[2]*lf,nominal[2]*uf), \
            (nominal[3]*lf,nominal[3]*uf)]


    def done_test_ncr(self):
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
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


    def get_model_problem_algorithm(self, config):
        algorithm = config["algorithm_setup"](None)
        data = config["data_setup"]()
        model = config["model_setup"]()
        problem = config["problem_setup"](model, data["calib"])
        return model, problem, algorithm


    def do_experiment_setup(self):
        config = sekrbi.do_experiment_setup_0_60()
        config["algorithm_setup"] = sekrbi.do_algorithm_setup_using_slsqp_with_positivity
        return config


    def do_experiment_setup_twice(self):
        config = sekrbi.do_experiment_setup_0_20_twice()
        #config["algorithm_setup"] = sekrbi.do_algorithm_setup_using_slsqp_with_positivity
        return config


    # WIP remove hard-coded sum_squared_residuals_st
    def dn_test_calibration_twice_workflow(self):
        calibrated = woex.test_baseline_calibration(self.do_experiment_setup_twice, None, self)
        if True:
            wore.plot_tiled_trajectories_at_point(self.do_experiment_setup_twice(), calibrated)


    def dn_test_calibration_workflow_0_20(self):
        calibrated = woex.test_baseline_calibration(sekrbi.do_experiment_setup, None, self)
        if True:
            wore.plot_tiled_trajectories_at_point(sekrbi.do_experiment_setup(), calibrated)


if __name__ == "__main__":
    unittest.main()
