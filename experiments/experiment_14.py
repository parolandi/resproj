
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
        return model, problem, algorithm

    
    def do_appy_bounds(self, nominal, problem):
        lf = 1E-2
        uf = 1E+2
        problem["bounds"] = [ \
            (nominal[0]*lf,nominal[0]*uf), \
            (nominal[1]*lf,nominal[1]*uf), \
            (nominal[2]*lf,nominal[2]*uf), \
            (nominal[3]*lf,nominal[3]*uf)]
        bounds = [[1.8560954071217014e-05, 0.00028822938131456123], [5999964.775229332, 5999999.3480375186], [0.0033295619005827282, 0.040367992439463547], [0.62924327562778315, 6.2924327562778313]]
        fc = 5
        problem["bounds"][0] = [bounds[0][0]/fc,bounds[0][1]*fc]
        problem["bounds"][1] = [bounds[1][0]/fc,bounds[1][1]*fc]
        problem["bounds"][2] = [bounds[2][0]/fc,bounds[2][1]*fc]
        problem["bounds"][3] = [bounds[3][0]/fc,bounds[3][1]*fc]
        

    
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
        algorithm_mc["number_of_trials"] = 80000

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
        replco.plot_combinatorial_region_projections(numpy.transpose(actual["decision_variables"]))


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
        replco.plot_combinatorial_region_projections(numpy.transpose(c))
        #repl.plot_scatter(numpy.transpose(c)[0], numpy.transpose(c)[3], None)
        

    def dn_test_troubleshoot1(self):
        best_point = {}
        best_point['objective_function'] = 10424.524182305697
        best_point['decision_variables'] = [1.58183747e-04, 5.99999935e+06, 3.32956190e-02, 6.29243276e-01]
        model, problem, algorithm = self.do_setup()
        
        mmdu.apply_decision_variables_to_parameters(best_point, model, problem)
        ssr = ecr.compute_f_constraint( \
            best_point["objective_function"],
            problem["outputs"],
            len(problem["parameter_indices"]),
            problem["confidence_region"]["confidence"])
        problem["confidence_region"]["ssr"] = ssr
        print(ssr)
        return
        if True:
            self.do_appy_bounds(best_point["decision_variables"], problem)
        logging.info(problem["bounds"])
        #param_index = 0
        #interval, status = ecr.compute_nonlinear_confidence_interval_extremal(model, problem, algorithm, param_index)
        #logging.info(interval)
        #logging.info(status)
        param_index = 1
        interval, status = ecr.compute_nonlinear_confidence_interval_extremal(model, problem, algorithm, param_index)
        logging.info(interval)
        logging.info(status)
        

if __name__ == "__main__":
    unittest.main()
    