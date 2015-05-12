
import unittest
import setups.kremlingetal_bioreactor as skb

import copy

import models.model_data as mmd
import setups.setup_data as ssd
import setups.setup_data_utils as ssdu
import workflows.protocols as wpr
import workflows.workflow_data_utils as wwdu

import common.diagnostics as cd


'''
Full data set 111111
Covariance trace
Also calibrate with 111111 but calibrate-validate; e.g., 111000
0-20hr interval
'''
class TestExperiment06(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment06, self).__init__(*args, **kwargs)
        self.do_plotting = False
    
    
    # TODO: reuse
    def do_experiment_setup(self):
        config = copy.deepcopy(ssd.experiment_setup)
        config["algorithm_setup"] = skb.do_algorithm_setup
        config["data_setup"] = skb.do_get_published_data_spliced_111111
        config["model_setup"] = skb.do_model_setup_model_B
#        config["problem_setup"] = skb.do_problem_setup
        config["protocol_setup"] = skb.do_protocol_setup
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        # TODO: () or not ()?
        config["sensitivity_setup"] = skb.do_sensitivity_setup()
        return config

    
    def do_experiment_setup_with_covariance_1(self):
        config = self.do_experiment_setup_0_20()
        config["problem_setup"] = skb.do_problem_setup_with_covariance_1
        return config

    
    def do_experiment_setup_with_covariance_2(self):
        config = self.do_experiment_setup_0_20()
        config["problem_setup"] = skb.do_problem_setup_with_covariance_2
        return config

    
    def test_protocol_basic_workflow(self):
        config = self.do_experiment_setup_with_covariance_1()

        _, _, problem_data, _ = ssdu.apply_config(config)
        reference_point = dict(mmd.optimisation_problem_point)
        reference_point["decision_variables"] = copy.deepcopy(problem_data["parameters"])
                
        actual = wpr.do_basic_workflow_at_solution_point(config, reference_point)
        expected = 0.892164390019673
        self.assertAlmostEquals(actual["ssr"], expected, 12)


    def test_protocol_sensitivity_based_workflow(self):
        config = self.do_experiment_setup_with_covariance_1()

        _, _, problem_data, _ = ssdu.apply_config(config)
        reference_point = dict(mmd.optimisation_problem_point)
        reference_point["objective_function"] = 0.045095700772591826
        reference_point["decision_variables"] = copy.deepcopy(problem_data["parameters"])

        actual = wpr.do_sensitivity_based_workflow_at_solution_point(config, reference_point)
        expected = [1.02735112e-04, 1.02405323e+08, 1.62582326e+00, 2.11443818e+00]
        delta = [0.00000001e-04, 0.00000001e+08, 0.00000001e+00, 0.00000001e+00]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 


    def test_protocol_calibration_and_basic_plus_sensitivity_based_workflow(self):
        config = self.do_experiment_setup_with_covariance_2()

        solution_point = wpr.do_calibration_and_compute_performance_measure(config)
        actual = solution_point["objective_function"]
        expected = 55.73031631952742
        self.assertAlmostEquals(actual, expected, 12)
        actual = solution_point["decision_variables"]
        expected = [7.06036656e-05, 5.95280934e+06, 7.86546429e-03, 5.61758623e-01]
        deltas = [0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-01]
        [self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]

        calib_results = wpr.do_basic_workflow_at_solution_point(config, solution_point)
        actual = calib_results
        expected = 55.73031631952742
        self.assertAlmostEquals(actual["ssr"], expected, 12)

        sens_calib_results = wpr.do_sensitivity_based_workflow_at_solution_point(config, solution_point)
        actual = sens_calib_results
        expected = [1.03901951e-04, 5.54043478e+07, 1.32527820e-01, 2.39891384e+02]
        delta = [0.00000001e-04, 0.00000001e+07, 0.00000001e-01, 0.00000001e+02]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 
        cd.print_decision_variables_and_objective_function(solution_point)
        wwdu.print_system_based_point_results(calib_results)
        wwdu.print_sensitivity_based_point_results(sens_calib_results)


    def test_protocol_calibration_and_validation(self):
        """
        Calibrate with 111111 but proceed to compute calibration-validation metrics with 111000
        """
        config = self.do_experiment_setup_with_covariance_2()
        solution_point = wpr.do_calibration_and_compute_performance_measure(config)
        
        config["data_setup"] = skb.do_get_published_data_spliced_111000
        calib_results = wpr.do_basic_workflow_at_solution_point(config, solution_point)
        sens_calib_results = wpr.do_sensitivity_based_workflow_at_solution_point(config, solution_point)
        wwdu.print_system_based_point_results(calib_results)
        wwdu.print_sensitivity_based_point_results(sens_calib_results)
        ssdu.set_next_protocol_step(config)
        valid_results = wpr.do_basic_workflow_at_solution_point(config, solution_point)
        sens_valid_results = wpr.do_sensitivity_based_workflow_at_solution_point(config, solution_point)
        wwdu.print_system_based_point_results(valid_results)
        wwdu.print_sensitivity_based_point_results(sens_valid_results)
        
        
if __name__ == "__main__":
    unittest.main()
