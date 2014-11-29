
import unittest
import setups.kremlingetal_bioreactor as skb

import copy

import experiments.protocols as epr
import metrics.ordinary_differential as mod
import models.model_data as mmd
import setups.setup_data as ssd
import setups.setup_data_utils as ssdu


class TestExperiment05(unittest.TestCase):


    def do_experiment_setup(self):
        config = dict(ssd.experiment_setup)
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup
        config["sensitivity_setup"] = skb.do_sensitivity_setup()
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
        expected = 0.02094963117201898
        self.assertAlmostEquals(actual["objective_function"], expected, 12)


    # test regression
    def test_protocol_workflow_at_nominal_point(self):
        config = self.do_experiment_setup()

        _, _, problem_data, _ = ssdu.apply_config(config)
        reference_point = dict(mmd.optimisation_problem_point)
        reference_point["decision_variables"] = copy.deepcopy(problem_data["parameters"])
                
        actual = epr.do_basic_workflow_at_solution_point(config, reference_point)
        expected = 0.045095700772591826
        self.assertAlmostEquals(actual["ssr"], expected, 12)


    # test regression
    def test_protocol_calibration_with_splicing(self):
        config = self.do_experiment_setup_splicing()
        actual = epr.do_calibration_and_compute_performance_measure(config)
        expected = 0.013033454937278158
        self.assertAlmostEquals(actual["objective_function"], expected, 12)


    # test regression
    def test_protocol_calibration_and_workflow_at_nominal_point_without_splicing(self):
        config = self.do_experiment_setup()
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "donot"

        _, _, problem_data, _ = ssdu.apply_config(config)
        reference_point = dict(mmd.optimisation_problem_point)
        reference_point["objective_function"] = 0.045095700772591826
        reference_point["decision_variables"] = copy.deepcopy(problem_data["parameters"])

        actual = epr.do_sensitivity_based_workflow_at_solution_point(config, reference_point)
        expected = [1.86329053e-14, 6.54341701e+08, 1.08977640e-13, 8.82897129e-13]
        delta = [0.00000001e-14, 0.00000001e+08, 0.00000001e-13, 0.00000001e-13]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 

    
    # test regression
    def test_protocol_calibration_and_workflow_at_solution_point_without_splicing(self):
        config = self.do_experiment_setup()
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "donot"
        solution_point = epr.do_calibration_and_compute_performance_measure(config)

        actual = solution_point["objective_function"]
        expected = 0.02094963117201898
        self.assertAlmostEquals(actual, expected, 12)
        actual = epr.do_basic_workflow_at_solution_point(config, solution_point)
        self.assertAlmostEquals(actual["ssr"], expected, 12)

        actual = epr.do_sensitivity_based_workflow_at_solution_point(config, solution_point)
        expected = [4.02126839e-15, 1.41217032e+08, 2.35190558e-14,  1.90542820e-13]
        delta = [0.00000001e-15, 0.00000001e+08, 0.00000001e-14, 0.00000001e-13]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 

    
if __name__ == "__main__":
    unittest.main()
