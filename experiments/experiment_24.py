
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
Splicing yes15-no5-yes10
Calculate and test nonlinear confidence region at high confidence
#Calculate and test nonlinear confidence region at low confidence
#Calculate and test approximate linear confidence region at low/high confidence
See also: exp-19
'''

# WIP: 2015-06-28; extract from exp-14
class TestExperiment24(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment24, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-24: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-24: finish")
        logging.info(codi.get_date_and_time())


    def test_nonlinear_confidence_region(self):
        logging.debug("experiments.experiment_24.test_calibration_and_validation")
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yes15no5yes10(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yes15no5yes10(basepoint)
        baseline["number_of_points"] = 0
        # [4, 8], [9, 9], [9, 8], [9, 8]
        baseline["intervals"] = [ \
            [7.2207627684700415e-06, 6.7861354646627067e-05], \
            [5783466.5054046102, 17147656.326588582], \
            [0.0011137464633125852, 0.11137464633125851], \
            [0.0053282484372208869, 0.20302644400404513]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "Exp-24: NCR benchmark model (95%)"
        
        experiment = sekrbitoo.do_protocol_setup_0_60_yes15n05yes10
        woex.test_calibration_with_nonlinear_confidence_region(experiment(), baseline, self)


if __name__ == "__main__":
    unittest.main()
