
import unittest
import setups.kremlingetal_bioreactor as skb

import copy
import numpy
import time

import common.diagnostics as cd
import common.utilities as cu
import data.generator as dg
import results.plot_tiles as rpt
import results.plot as rpl
import setups.setup_data as ssd
import solvers.monte_carlo_multiple_initial_value as smiv


'''
Prediction uncertainty
Splicing at 111000
Covariance trace ~10%
'''
class TestExperiment11(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment11, self).__init__(*args, **kwargs)
        self.do_plotting = False

    
    def do_experiment_setup(self):
        config = copy.deepcopy(ssd.experiment_setup)
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_111111
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup_with_covariance_2
        config["protocol_setup"] = skb.do_protocol_setup
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        # TODO: () or not ()?
        config["sensitivity_setup"] = skb.do_sensitivity_setup()
        return config


    def do_experiment_setup_with_exclude(self):
        config = self.do_experiment_setup()
        config["problem_setup"] = skb.do_problem_setup_with_exclude_with_covariance_2
        return config

    
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
        config = self.do_experiment_setup()
        no_volume = 1

        model = config["model_setup"]()
        data = config["data_setup"]()
        problem = config["problem_setup"](model, data["calib"])
        algorithm = self.do_algorithm_setup()

        wall_time0 = time.time()
        result = smiv.solve(model, problem, algorithm)
        wall_time = time.time() - wall_time0
        cd.print_wall_time_message(wall_time)
        ensembles = result["succeeded"]["trajectories"][:,no_volume:,:]
        
        expected = numpy.ones(ensembles.shape[1])
        actual = cu.get_maximum_absolute_ensemble_values(ensembles)
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual.flatten(), expected.flatten())]

        if self.do_plotting:     
            plot_config = {}
            plot_config["output_names"] = skb.do_labels()[no_volume:]
            errors, _ = dg.compute_measurement_errors(problem, data)
            rpt.plot_ensemble_trajectories(problem["time"], ensembles, problem["outputs"], errors, plot_config)
            rpt.show_all()
            rpl.plot_histogram_cutoff_by_count(result["succeeded"]["objective_function"], 20, 3)


if __name__ == "__main__":
    unittest.main()