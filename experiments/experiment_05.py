
import unittest
import setups.kremlingetal_bioreactor as skb

import copy
import numpy

import workflows.protocols as wpr
import metrics.ordinary_differential as mod
import models.model_data as mmd
import setups.setup_data as ssd
import setups.setup_data_utils as ssdu

'''
Verify metric at nominal point
Calibrate with full data
Calibrate with 111000 splicing
'''
class TestExperiment05(unittest.TestCase):


    def do_experiment_setup(self):
        config = dict(ssd.experiment_setup)
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup
        config["sensitivity_setup"] = skb.do_sensitivity_setup()
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_111111
        config["protocol_setup"] = skb.do_protocol_setup
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "donot"
        return config

    
    def do_experiment_setup_splicing(self):
        config = dict(ssd.experiment_setup)
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup
        config["sensitivity_setup"] = skb.do_sensitivity_setup()
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_111000
        config["protocol_setup"] = skb.do_protocol_setup
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "donot"
        return config

    
    # TODO: extract as workflow?
    '''
    Compute sum squared residuals, nominal point
    '''
    def test_verification(self):
        model_data = skb.do_model_setup_model_B()
        data_data = skb.do_get_published_data_spliced_111111()
        problem_data = skb.do_problem_setup(model_data, data_data["calib"])

        actual = mod.sum_squared_residuals_st(None, None, model_data, problem_data)
        expected = 0.045095700772591826
        self.assertAlmostEqual(actual, expected, 12)


    '''
    Calibrate, use full data set
    '''
    def test_protocol_calibration_without_splicing(self):
        config = self.do_experiment_setup()
        actual = wpr.do_calibration_and_compute_performance_measure(config)
        expected = 0.02094963117201898
        self.assertAlmostEquals(actual["objective_function"], expected, 12)
        expected = numpy.array([7.00537514e-05, 6.28707509e+06, 7.21106611e-03, 2.84514441e+01])
        deltas = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e+01])
        [self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual["decision_variables"], expected, deltas)]


    '''
    Calibrate, use 111000-spliced data set
    '''
    def test_protocol_calibration_with_splicing(self):
        config = self.do_experiment_setup_splicing()
        actual = wpr.do_calibration_and_compute_performance_measure(config)
        expected = 0.013033454937278158
        self.assertAlmostEquals(actual["objective_function"], expected, 12)
        expected = numpy.array([6.94673782e-05, 6.89584538e+06, 6.28171859e-03, 1.80509631e+00])
        deltas = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e+00])
        [self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual["decision_variables"], expected, deltas)]

    
    '''
    Basic protocol, nominal point, use full data set
    '''
    def test_protocol_basic_workflow_without_splicing(self):
        config = self.do_experiment_setup()

        _, _, problem_data, _ = ssdu.apply_config(config)
        reference_point = dict(mmd.optimisation_problem_point)
        reference_point["decision_variables"] = copy.deepcopy(problem_data["parameters"])
                
        actual = wpr.do_basic_workflow_at_solution_point(config, reference_point)
        expected = 0.045095700772591826
        self.assertAlmostEquals(actual["ssr"], expected, 12)


    '''
    Sensitivity protocol, nominal point, use full data set
    '''
    def test_protocol_sensitivity_based_workflow_without_splicing(self):
        config = self.do_experiment_setup()

        _, _, problem_data, _ = ssdu.apply_config(config)
        reference_point = dict(mmd.optimisation_problem_point)
        reference_point["objective_function"] = 0.045095700772591826
        reference_point["decision_variables"] = copy.deepcopy(problem_data["parameters"])

        actual = wpr.do_sensitivity_based_workflow_at_solution_point(config, reference_point)
        expected = [1.86329053e-14, 6.54341701e+08, 1.08977640e-13, 8.82897129e-13]
        delta = [0.00000001e-14, 0.00000001e+08, 0.00000001e-13, 0.00000001e-13]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 

    
    '''
    Calibration followed by basis and sensitivity-based protocols using the full data set
    '''
    def test_protocol_calibration_and_basic_plus_sensitivity_based_workflow_without_splicing(self):
        config = self.do_experiment_setup()

        solution_point = wpr.do_calibration_and_compute_performance_measure(config)
        actual = solution_point["objective_function"]
        expected = 0.02094963117201898
        self.assertAlmostEquals(actual, expected, 12)

        actual = wpr.do_basic_workflow_at_solution_point(config, solution_point)
        self.assertAlmostEquals(actual["ssr"], expected, 12)

        actual = wpr.do_sensitivity_based_workflow_at_solution_point(config, solution_point)
        expected = [4.02126839e-15, 1.41217032e+08, 2.35190558e-14,  1.90542820e-13]
        delta = [0.00000001e-15, 0.00000001e+08, 0.00000001e-14, 0.00000001e-13]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 

    
if __name__ == "__main__":
    unittest.main()
