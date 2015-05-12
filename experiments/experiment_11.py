
import unittest
import setups.kremlingetal_bioreactor as skb

import numpy
import time

import common.diagnostics as cd
import common.utilities as cu
import data.generator as dg
import results.plot_tiles as rpt
import results.plot as rpl
import setups.setup_data_utils as sesedaut
import solvers.monte_carlo_multiple_initial_value as smiv


'''
Kremling bioreactor
Prediction uncertainty
Splicing at 111000
Covariance trace ~10%
'''
class TestExperiment11(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment11, self).__init__(*args, **kwargs)
        self.do_plotting = True

    
    def do_experiment_setup(self):
        return skb.do_experiment_setup_0_60()


    def do_algorithm_setup(self):
        algorithm = dict(smiv.montecarlo_multiple_simulation_params)
        nominals = [7.23232059e-05, 6.00000000e+06, 1.67959956e-02, 1.00866368e-02]
        # nominal confidence intervals
        _ = [7.55459755277e-08, 9.72361400229e+16, 4.25111892419, 4768.80323967]
        conf_intvs = [7.55459755277e-08 / nominals[0], 0.5, 0.5, 0.5]
        algorithm["decision_variable_ranges"] = []
        for ii in range(len(nominals)):
            algorithm["decision_variable_ranges"].append( \
                (nominals[ii]*(1-conf_intvs[ii]), nominals[ii]*(1+conf_intvs[ii])))
        algorithm["number_of_trials"] = 100
        algorithm["subsolver_params"]["method"] = "Nelder-Mead"
        return algorithm

    
    def test_prediction_uncertainty(self):
        no_volume = 1

        model, data, problem, _ = sesedaut.get_model_data_problem_algorithm(self.do_experiment_setup())
        algorithm = self.do_algorithm_setup()

        wall_time0 = time.time()
        result = smiv.solve(model, problem, algorithm)
        wall_time = time.time() - wall_time0
        cd.print_wall_time_message(wall_time)
        ensembles = result["succeeded"]["trajectories"][:,no_volume:,:]
        
        actual = cu.get_maximum_absolute_ensemble_values(ensembles)
        self.assertAlmostEqual(actual[0,2], 0.44510079, 8)
        self.assertAlmostEqual(actual[99,30], 1.50490147, 8)

        if self.do_plotting:     
            plot_config = {}
            plot_config["output_names"] = skb.do_labels()[no_volume:]
            errors, _ = dg.compute_measurement_errors(problem, data)
            rpt.plot_ensemble_trajectories(problem["time"], ensembles, problem["outputs"], errors, plot_config)
            rpl.plot_histogram_cutoff_by_count(result["succeeded"]["objective_function"], 20, 3)
            rpt.show_all()


if __name__ == "__main__":
    unittest.main()