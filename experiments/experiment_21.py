
import unittest
import setups.kremlingetal_bioreactor as sekrbi
import setups.kremlingetal_bioreactor_unlegacy as sekrbitoo
import experiments.baselines as exba

import logging

import common.diagnostics as codi
import common.environment as coen
import results.plot_data as replda
import results.plot_utils as replut
import workflows.experiments as woex


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
Splicing yes-no-yes
Calculate and test nonlinear confidence region at high confidence
#Calculate and test nonlinear confidence region at low confidence
Calculate and test approximate linear confidence region at high confidence
#Calculate and test approximate linear confidence region at low confidence
See also: exp-17
'''

# WIP: 2015-06-28; extract from exp-14
class TestExperiment21(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment21, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-21: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-21: finish")
        logging.info(codi.get_date_and_time())


    def get_baseline_nonlinear_confidence_region(self):
        baseline = dict(woex.calib_valid_baseline)
        baseline["plotdata"] = dict(replda.plot_data)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yesnoyes(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yesnoyes(basepoint)
        baseline = replut.set_window_title(baseline, "Exp-21: NCR benchmark model (95%)")
        return baseline
        
        
    def test_nonlinear_confidence_region(self):
        logging.debug("experiments.experiment_21.test_calibration_and_validation")
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        baseline = self.get_baseline_nonlinear_confidence_region()
        experiment = sekrbitoo.do_protocol_setup_0_60_yesnoyes
        woex.test_calibration_with_nonlinear_confidence_region(experiment(), baseline, self)


    def get_baseline_linearised_confidence_region(self):
        baseline = dict(woex.calib_valid_baseline)
        baseline["plotdata"] = dict(replut.plda.plot_data)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yesnoyes(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yesnoyes(basepoint)
        baseline = exba.set_baseline_linconfreg_0_60_yesnoyes(baseline)
        baseline = replut.set_window_title(baseline, "Exp-21: LCR benchmark model (95%)")
        return baseline


    def test_linearised_confidence_region(self):
        logging.debug("experiments.experiment_21.test_linearised_confidence_region")
        baseline = self.get_baseline_linearised_confidence_region()
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesnoyes
        woex.test_calibration_with_linearised_confidence_region(experiment(), baseline, self)


if __name__ == "__main__":
    unittest.main()
