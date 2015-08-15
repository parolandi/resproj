
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
Splicing yes10-yes15-no5
Calculate and test nonlinear confidence region at high confidence
#Calculate and test nonlinear confidence region at low confidence
#Calculate and test approximate linear confidence region at low/high confidence
See also: exp-18
'''

# WIP: 2015-06-28; extract from exp-14
class TestExperiment23(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment23, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-23: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-23: finish")
        logging.info(codi.get_date_and_time())


    def test_nonlinear_confidence_region(self):
        logging.debug("experiments.experiment_23.test_calibration_and_validation")
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yes10yes15no5(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yes10yes15no5(basepoint)
        baseline["number_of_points"] = 0
        # [8, 9], [8, 9], [9, 4], [9, 9]
        baseline["intervals"] = [ \
            [8.3865274119544132e-05, 8.7361023095616056e-05], \
            [5759553.1188991377, 5776681.8321100501], \
            [0.0093196862993481545, 0.093196862993481538], \
            [0.0043275124884777994, 0.43275124884777993]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "Exp-23: NCR benchmark model (95%)"
        
        experiment = sekrbitoo.do_protocol_setup_0_60_yes10yes15no5
        woex.test_calibration_with_nonlinear_confidence_region(experiment(), baseline, self)


if __name__ == "__main__":
    unittest.main()
