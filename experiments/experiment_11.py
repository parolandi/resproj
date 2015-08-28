
import unittest
import setups.kremlingetal_bioreactor as skb

import logging
import time

import common.diagnostics as codi
import common.environment as coen
import common.utilities as cu
import data.generator as dg
import results.plot_tiles as rpt
import results.plot as rpl
import setups.setup_data_utils as sesedaut
import solvers.monte_carlo_multiple_initial_value as smiv


'''
Kremling bioreactor
Prediction uncertainty
No splicing
Covariance trace ~10%
Both 0-20 and 0-60
'''
class TestExperiment11(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment11, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-11: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-11: finish")
        logging.info(codi.get_date_and_time())

    
    def do_algorithm_setup(self):
        algorithm = dict(smiv.montecarlo_multiple_simulation_params)
        nominals = [7.23232059e-05, 6.00000000e+06, 1.67959956e-02, 1.00866368e-02]
        conf_intvs = [7.55459755277e-08 / nominals[0], 0.5, 0.5, 0.5]
        algorithm["decision_variable_ranges"] = []
        for ii in range(len(nominals)):
            algorithm["decision_variable_ranges"].append( \
                (nominals[ii]*(1-conf_intvs[ii]), nominals[ii]*(1+conf_intvs[ii])))
        algorithm["number_of_trials"] = 100
        algorithm["subsolver_params"]["method"] = "Nelder-Mead"
        algorithm["enable_trajectories"] = True
        return algorithm

    
    def do_test_prediction_uncertainty(self, config, baseline):
        no_volume = 1

        model, data, problem, _ = sesedaut.get_model_data_problem_algorithm_with_calib(config)
        algorithm = self.do_algorithm_setup()

        wall_time0 = time.time()
        result = smiv.solve(model, problem, algorithm)
        wall_time = time.time() - wall_time0
        codi.print_wall_time_message(wall_time)
        ensembles = result["succeeded"]["trajectories"][:,no_volume:,:]
        
        actual = cu.get_maximum_absolute_ensemble_values(ensembles)
        self.assertAlmostEqual(actual[0,2], baseline[0], 8)
        self.assertAlmostEqual(actual[99,-1], baseline[1], 8)

        if self.do_plotting:     
            plot_config = {}
            plot_config["output_names"] = skb.do_labels()[no_volume:]
            errors, _ = dg.compute_measurement_errors(problem, data)
            rpt.plot_ensemble_trajectories(problem["time"], ensembles, problem["outputs"], errors, plot_config)
            rpl.plot_histogram_cutoff_by_count(result["succeeded"]["objective_function"], 20, 3)
            rpt.show_all()


    def test_prediction_uncertainty_0_60(self):
        baseline = []
        baseline.append(0.44510079)
        baseline.append(1.50490147)
        self.do_test_prediction_uncertainty(skb.do_experiment_setup_0_60(), baseline)


    def test_prediction_uncertainty_0_20(self):
        baseline = []
        baseline.append(0.44510079)
        baseline.append(0.57332800)
        self.do_test_prediction_uncertainty(skb.do_experiment_setup_0_20(), baseline)


if __name__ == "__main__":
    unittest.main()