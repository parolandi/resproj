
import unittest
import setups.kremlingetal_bioreactor as skb

import experiments.protocols as epr
import metrics.ordinary_differential as mod
import setups.setup_data as ssd


class TestExperiment05(unittest.TestCase):


    def do_experiment_setup(self):
        config = dict(ssd.experiment_setup)
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_111111
        config["protocol_setup"] = skb.do_protocol_setup
        return config

    
    def do_experiment_setup_splicing(self):
        config = dict(ssd.experiment_setup)
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_111000
        config["protocol_setup"] = skb.do_protocol_setup
        return config

    
    # TODO: extract as workflow?
    '''
    Compute sum squared residuals 
    '''
    # test regression
    def test_verification(self):
        model_data = skb.do_model_setup_model_B()
        data_data = skb.do_get_published_data_spliced_111111()
        problem_data = skb.do_problem_setup(model_data, data_data["calib"])

        actual = mod.sum_squared_residuals_st(None, None, model_data, problem_data)
        expected = 0.045095700772591826
        self.assertAlmostEqual(actual, expected, 12)


    # test regression
    def test_protocol_calibration_without_splicing(self):
        config = self.do_experiment_setup()
        actual = epr.do_calibration_and_compute_performance_measure(config)
        expected = 0.020948632939275735
        self.assertAlmostEquals(actual, expected, 12)


    # TODO: at solution point
    # test regression
    def test_protocol_workflow_at_solution_point(self):
        config = self.do_experiment_setup()
        actual = epr.do_basic_workflow_at_solution_point(config)
        expected = 0.045095700772591826
        self.assertAlmostEquals(actual["ssr"], expected, 12)


    # test regression
    def test_protocol_calibration_with_splicing(self):
        config = self.do_experiment_setup_splicing()
        actual = epr.do_calibration_and_compute_performance_measure(config)
        expected = 0.01302438324230857
        self.assertAlmostEquals(actual, expected, 12)


if __name__ == "__main__":
    unittest.main()
