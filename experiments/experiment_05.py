
import unittest
import setups.kremlingetal_bioreactor as skb

import copy
import logging
import numpy

import common.diagnostics as codi
import common.environment as coen
import metrics.ordinary_differential as mod
import models.model_data as mmd
import setups.setup_data as ssd
import setups.setup_data_utils as ssdu
import workflows.protocols as wpr


'''
Full data set 111111
No covariance trace
'''
class TestExperiment05(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment05, self).__init__(*args, **kwargs)
        self.plotting = coen.get_doing_plotting()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-05: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-05: finish")
        logging.info(codi.get_date_and_time())
    
    
    def do_experiment_setup(self):
        config = copy.deepcopy(ssd.experiment_setup)
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_111111
        config["model_setup"] = skb.do_model_setup_model_B
        config["problem_setup"] = skb.do_problem_setup
        config["protocol_setup"] = skb.do_protocol_setup
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        # TODO: () or not ()?
        config["sensitivity_setup"] = skb.do_sensitivity_setup()
        return config

    
    # TODO: extract as workflow?
    '''Compute sum squared residuals, nominal point'''
    def test_verification(self):
        model_data = skb.do_model_setup_model_B()
        data_data = skb.do_get_published_data_spliced_111111()
        problem_data = skb.do_problem_setup(model_data, data_data["calib"])

        actual = mod.sum_squared_residuals_st(None, None, model_data, problem_data)
        expected = 0.045095700772591826
        self.assertAlmostEqual(actual, expected, 12)


    def test_protocol_calibration(self):
        config = self.do_experiment_setup()
        actual = wpr.do_calibration_and_compute_performance_measure(config)
        expected = 0.020948695742714324
        self.assertAlmostEquals(actual["objective_function"], expected, 12)
        expected = numpy.array([7.00464849e-05, 6.27834699e+06, 7.22037461e-03, 3.67489807e+02])
        deltas = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e+02])
        [self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual["decision_variables"], expected, deltas)]


    def test_protocol_basic_workflow(self):
        config = self.do_experiment_setup()

        _, _, problem_data, _ = ssdu.apply_config(config)
        reference_point = dict(mmd.optimisation_problem_point)
        reference_point["decision_variables"] = copy.deepcopy(problem_data["parameters"])
                
        actual = wpr.do_basic_workflow_at_solution_point(config, reference_point)
        expected = 0.045095700772591826
        self.assertAlmostEquals(actual["ssr"], expected, 12)


    def test_protocol_sensitivity_based_workflow(self):
        config = self.do_experiment_setup()

        _, _, problem_data, _ = ssdu.apply_config(config)
        reference_point = dict(mmd.optimisation_problem_point)
        reference_point["objective_function"] = 0.892164390019673
        reference_point["decision_variables"] = copy.deepcopy(problem_data["parameters"])

        actual = wpr.do_sensitivity_based_workflow_at_solution_point(config, reference_point)
        expected = [1.02735112e-04, 1.02405323e+08, 1.62582326e+00, 2.11443818e+00]
        delta = [0.00000001e-04, 0.00000001e+08, 0.00000001e+00, 0.00000001e+00]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 

    
    '''
    Calibration followed by basic and sensitivity-based protocols using the full data set
    Regressed between 2014-11-30 and 2014-12-12
    '''
    def regression_test_protocol_calibration_and_basic_plus_sensitivity_based_workflow(self):
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


    '''
    Calibration followed by basic and sensitivity-based protocols using the full data set
    Spin-off after regression between 2014-11-30 and 2014-12-12
    '''
    def test_protocol_calibration_and_basic_plus_sensitivity_based_workflow(self):
        config = self.do_experiment_setup()

        solution_point = wpr.do_calibration_and_compute_performance_measure(config)
        actual = solution_point["objective_function"]
        expected = 0.020948695742714324
        self.assertAlmostEquals(actual, expected, 12)
        actual = solution_point["decision_variables"]
        expected = numpy.array([7.00464849e-05, 6.27834699e+06, 7.22037461e-03, 3.67489807e+02])
        deltas = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e+02])
        [self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]

        actual = wpr.do_basic_workflow_at_solution_point(config, solution_point)
        expected = 0.020948695742714324
        self.assertAlmostEquals(actual["ssr"], expected, 12)

        actual = wpr.do_sensitivity_based_workflow_at_solution_point(config, solution_point)
        expected = [1.01561007e-04, 5.23880530e+07, 6.86689774e-02, 1.05672415e+05]
        delta = [0.00000001e-04, 0.00000001e+07, 0.00000001e-02, 0.00000001e+05]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 


if __name__ == "__main__":
    unittest.main()
