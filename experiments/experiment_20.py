
import unittest
import setups.kremlingetal_bioreactor_unlegacy as sekrbitoo
import experiments.baselines as exba

import logging

import common.diagnostics as codi
import common.environment as coen
import results.plot_data as replda
import workflows.experiments as woex


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
No splicing
Calculate and test nonlinear confidence region at high confidence
#Calculate and test nonlinear confidence region at low confidence
#Calculate and test approximate linear confidence region at low/high confidence
'''

# WIP: 2015-06-28; extract from exp-14
class TestExperiment20(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment20, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-20: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-20: finish")
        logging.info(codi.get_date_and_time())


    def test_nonlinear_confidence_region(self):
        logging.debug("experiments.experiment_20.test_nonlinear_confidence_region")
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60(basepoint)
        basepoint = exba.set_baseline_eps_0_60(basepoint)
        baseline["number_of_points"] = 0
        # [[0, 0], [8, 0], [9, 8], [9, 9]]
        baseline["intervals"] = [ \
            [7.1815198110426653e-05, 7.2828378864918741e-05], \
            [5927979.0165858017, 5928271.2840146916], \
            [0.0012124961140420856, 0.12124961140420856], \
            [0.0017173506980212713, 0.1717350698021271]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "Exp-20: NCR benchmark model (95%)"
        
        experiment = sekrbitoo.do_protocol_setup_0_60_default
        woex.test_calibration_with_nonlinear_confidence_region(experiment(), baseline, self)


if __name__ == "__main__":
    unittest.main()