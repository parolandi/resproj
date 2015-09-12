import unittest
#import setups.kremlingetal_bioreactor as sekrbi
import setups.kremlingetal_bioreactor_unlegacy as sekrbitoo
import experiments.baselines as exba

import logging

import common.diagnostics as codi
import common.environment as coen
import results.plot_utils as replut
import workflows.experiments as woex

class TestRunExecutive(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRunExecutive, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("run-executive: start")
        logging.info(codi.get_date_and_time())

    def __del__(self):
        logging.info("run-executive: finish")
        logging.info(codi.get_date_and_time())

    def get_baseline_nonlinear_confidence_region(self):
        baseline = dict(woex.calib_valid_baseline)
        baseline["plotdata"] = dict(replut.plda.plot_data)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yesyesno(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yesyesno(basepoint)
        baseline = exba.set_baseline_nonlinconfreg_0_60_yesyesno(baseline)
        baseline = replut.set_window_title(baseline, "Run-executive: NCR benchmark model (95%)")
        return baseline
    

    def test_nonlinear_confidence_region(self):
        logging.debug("experiments.run_executive.test_nonlinear_confidence_region: 0_60_yesnoyes")
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        baseline = self.get_baseline_nonlinear_confidence_region()
        experiment = sekrbitoo.do_protocol_setup_0_60_any_compute
        woex.test_calibration_with_nonlinear_confidence_region(experiment(), baseline, self)

    
if __name__ == "__main__":
    unittest.main()