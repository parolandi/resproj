
import unittest
import setups.kremlingetal_bioreactor as skb

import copy
import numpy

import models.model_data as mmd
import setups.setup_data as ssd
import setups.setup_data_utils as ssdu
import workflows.protocols as wpr
import workflows.workflow_data_utils as wwdu

import common.diagnostics as cd


'''
Full data set 111111
Covariance trace
'''
class TestExperiment06(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment06, self).__init__(*args, **kwargs)
        self.do_plotting = False
    
    
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
        config = self.do_experiment_setup()
        config["problem_setup"] = skb.do_problem_setup_with_covariance_1
        return config

    
    def do_experiment_setup_with_covariance_2(self):
        config = self.do_experiment_setup()
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
        expected = [1.86329053e-14, 6.54341701e+08, 1.08977640e-13, 8.82897129e-13]
        delta = [0.00000001e-14, 0.00000001e+08, 0.00000001e-13, 0.00000001e-13]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 


    def test_protocol_calibration_and_basic_plus_sensitivity_based_workflow(self):
        config = self.do_experiment_setup_with_covariance_2()

        solution_point = wpr.do_calibration_and_compute_performance_measure(config)
        actual = solution_point["objective_function"]
        expected = 0.5573030504714559
        #self.assertAlmostEquals(actual, expected, 12)
        actual = solution_point["decision_variables"]
        expected = numpy.array([7.06065100e-05, 5.95442624e+06, 7.86537515e-03, 5.57347837e-01])
        deltas = numpy.array([0.00000001e-05, 0.00000001e+06, 0.00000001e-03, 0.00000001e-01])
        #[self.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]

        calib_results = wpr.do_basic_workflow_at_solution_point(config, solution_point)
        actual = calib_results
        expected = 0.5573030504714559
        #self.assertAlmostEquals(actual["ssr"], expected, 12)

        sens_calib_results = wpr.do_sensitivity_based_workflow_at_solution_point(config, solution_point)
        actual = sens_calib_results
        expected = [2.51917019317e-12, 2.04365259969e+12, 1.4122097917e-06, 2.49703886148e+01]
        delta = [0.00000001e-12, 0.00000001e+12, 0.00000001e-06, 0.00000001e+01]
        #[self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(actual["conf_intvs"], expected, delta)] 
        cd.print_decision_variables_and_objective_function(solution_point)
        wwdu.print_system_based_point_results(calib_results)
        wwdu.print_sensitivity_based_point_results(sens_calib_results)


if __name__ == "__main__":
#    unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestExperiment06("test_protocol_calibration_and_basic_plus_sensitivity_based_workflow_without_splicing_with_covariance"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
