
import unittest
import setups.kremlingetal_bioreactor as sekrbi
import setups.kremlingetal_bioreactor_unlegacy as sekrbiun

import logging

import common.diagnostics as codi
import common.environment as coen
import experiments.baselines as exba
import results.plot_data as replda
import results.plot_utils as replut
import workflows.experiments as woex


'''
Kremling bioreactor
Calculate and test nonlinear confidence region at low/high confidence
Calculate and test approximate linear confidence region at low/high confidence
0-20 hr interval
'''
class TestExperiment14(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment14, self).__init__(*args, **kwargs)
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-14: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-14: finish")
        logging.info(codi.get_date_and_time())

    
    def do_experiment_setup(self):
        config = sekrbi.do_experiment_setup_0_20()
        config["algorithm_setup"] = sekrbi.do_algorithm_setup_using_slsqp_with_positivity
        return config


    def do_experiment_setup_with_low_confidence(self):
        config = sekrbi.do_experiment_setup_0_20()
        config["problem_setup"] = sekrbi.do_problem_setup_with_covariance_2_and_low_confidence
        return config

    
    def get_baseline_nonlinear_confidence_region(self):
        baseline = dict(woex.calib_valid_baseline)
        baseline["plotdata"] = dict(replda.plot_data)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_20(basepoint)
        basepoint = exba.set_baseline_eps(basepoint)
        baseline = exba.set_baseline_nonlinconfreg_0_20(baseline)
        baseline = replut.set_window_title(baseline, "Exp-14: NCR benchmark model (25%)")
        return baseline

    
    def test_nonlinear_confidence_region(self):
        logging.debug("experiments.experiment_14.test_nonlinear_confidence_region")
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        baseline = self.get_baseline_nonlinear_confidence_region()
        woex.test_calibration_with_nonlinear_confidence_region( \
            sekrbiun.do_protocol_setup_0_20_default(), baseline, self)

    
    def get_baseline_nonlinear_confidence_region_low_confidence(self):
        baseline = dict(woex.calib_valid_baseline)
        baseline["plotdata"] = dict(replda.plot_data)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_20(basepoint)
        basepoint = exba.set_baseline_eps(basepoint)
        baseline = exba.set_baseline_nonlinconfreg_0_20_lowconf(baseline)
        baseline = replut.set_window_title(baseline, "Exp-14: NCR benchmark model (low-conf)")
        return baseline

    
    def test_nonlinear_confidence_region_low_confidence(self):
        logging.debug("experiments.experiment_14.test_nonlinear_confidence_region_low_confidence")
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        baseline = self.get_baseline_nonlinear_confidence_region_low_confidence()
        woex.test_calibration_with_nonlinear_confidence_region( \
            sekrbiun.do_protocol_setup_0_20_low_confidence(), baseline, self)


    def get_baseline_linearised_confidence_region(self):
        baseline = dict(woex.calib_valid_baseline)
        baseline["plotdata"] = dict(replda.plot_data)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_20(basepoint)
        basepoint = exba.set_baseline_eps(basepoint)
        baseline = exba.set_baseline_linconfreg_0_20(baseline)
        baseline = replut.set_window_title(baseline, "Exp-14: LCR benchmark model (95%)")
        return baseline


    def test_linearised_confidence_region(self):
        logging.debug("experiments.experiment_14.test_linearised_confidence_region")
        baseline = self.get_baseline_linearised_confidence_region()
        woex.test_calibration_with_linearised_confidence_region( \
            sekrbi.do_experiment_setup_0_20(), baseline, self)


    def get_baseline_linearised_confidence_region_low_confidence(self):
        baseline = dict(woex.calib_valid_baseline)
        baseline["plotdata"] = dict(replda.plot_data)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_20(basepoint)
        basepoint = exba.set_baseline_eps(basepoint)
        baseline = exba.set_baseline_linconfreg_0_20_lowconf(baseline)
        baseline = replut.set_window_title(baseline, "Exp-14: LCR benchmark model (25%)")
        return baseline


    def test_linearised_confidence_region_low_confidence(self):
        logging.debug("experiments.experiment_14.test_linearised_confidence_region_low_confidence")
        baseline = self.get_baseline_linearised_confidence_region_low_confidence()
        woex.test_calibration_with_linearised_confidence_region( \
            self.do_experiment_setup_with_low_confidence(), baseline, self)


if __name__ == "__main__":
    unittest.main()
