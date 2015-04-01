
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import metrics.ordinary_differential as mod
import models.model_data_utils as mmdu
import engine.confidence_regions as ecr
import results.plot as repl
import results.plot_data as replda
import solvers.least_squares as sls
import solvers.monte_carlo_multiple_initial_value as mcmiv
import workflows.reporting as wr

import results.plot_combinatorial as replco


class TestExperiment14(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment14, self).__init__(*args, **kwargs)
        self.do_plotting = False
        logging.basicConfig(filename='C:/workspace/resproj/app.log',level=logging.INFO)

    
    def do_experiment_setup(self):
        config = sekrbi.do_experiment_setup()
        config["algorithm_setup"] = sekrbi.do_algorithm_setup_using_slsqp_with_positivity
        return config


    def do_setup(self):
        config = self.do_experiment_setup()
        algorithm = config["algorithm_setup"](None)
        data = config["data_setup"]()
        model = config["model_setup"]()
        problem = config["problem_setup"](model, data["calib"])

        #algorithm = config["algorithm_setup"](None)
        #algorithm["initial_guesses"] = copy.deepcopy(numpy.asarray(problem["parameters"]))
        #algorithm["method"] = 'SLSQP'

        return model, problem, algorithm

    
    def do_appy_bounds(self, nominal, problem):
        lf = 1E-1
        uf = 1E+1
        problem["bounds"] = [ \
            (nominal[0]*lf,nominal[0]*uf), \
            (nominal[1]*lf,nominal[1]*uf), \
            (nominal[2]*lf,nominal[2]*uf), \
            (nominal[3]*lf,nominal[3]*uf)]

    
    def do_test_compute_nonlinear_confidence_region_points(self, setup, config, baseline):
        # setup regression
        model, problem, algorithm = setup()

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
        algorithm_mc["number_of_trials"] = 10

        if True:
            self.do_appy_bounds(best_point["decision_variables"], problem)
        logging.info(problem["bounds"])
        
        # do nonlin conf reg
        actual = ecr.compute_nonlinear_confidence_region_points_extremal( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        number_of_points = len(numpy.transpose(actual["objective_function"]))
        print("number of points", number_of_points)
        #self.assertEquals(number_of_points, baseline["number_of_points"])
        
        logging.info(actual)

        # plot nonlin conf reg
        if self.do_plotting:
            points = numpy.asarray(actual["decision_variables"])
            repl.plot_scatter(numpy.transpose(points)[0], numpy.transpose(points)[1], baseline["plotdata"])


    def test_it(self):
        baseline = {}
        baseline["number_of_points"] = 7834
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model"
        self.do_test_compute_nonlinear_confidence_region_points( \
            self.do_setup, self.do_experiment_setup, baseline)
        self.assertFalse(True)
        

    def dn_test_plot_it(self):
        c = numpy.loadtxt('C:/workspace/resproj/pnts.txt')
        #replco.plot_combinatorial_region_projections(numpy.transpose(c))
        repl.plot_scatter(numpy.transpose(c)[0], numpy.transpose(c)[2], None)
        

if __name__ == "__main__":
    unittest.main()