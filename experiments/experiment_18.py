import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging

import common.diagnostics as codi
import common.environment as coen
import experiments.baselines as exba
import workflows.experiments as woex
import workflows.reporting_unlegacy as wore

'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
Splicing yes10-yes15-no5
Calibration
See also: exp-23
'''
class TestExperiment18(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestExperiment18, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-18: start")
        logging.info(codi.get_date_and_time())

    def __del__(self):
        logging.info("exp-18: finish")
        logging.info(codi.get_date_and_time())

    def get_calibration_validation_baseline(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yes10yes15no5(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yes10yes15no5(basepoint)
        baseline["valid"]["point"]["objective_function"] = exba.get_baseline_point_0_60_yes10yes15no5()
        return baseline

    def get_calibration_validation_baseline_global(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yes10yes15no5_global(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yes10yes15no5(basepoint)
        baseline["valid"]["point"]["objective_function"] = exba.get_baseline_point_0_60_yes10yes15no5_global()
        return baseline

    
    def test_calibration_and_validation(self):
        logging.debug("experiments.experiment_18.test_calibration_and_validation")
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yes10yes15no5
        baseline = self.get_calibration_validation_baseline()
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
    def test_calibration_and_validation_global(self):
        logging.debug("experiments.experiment_18.test_calibration_and_validation_global")
        if self.do_quick_tests_only:
            codi.print_and_log_return_on_quick_tests_only()
            return
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yes10yes15no5_with_global_neldermead_100_10xpm
        baseline = self.get_calibration_validation_baseline_global()
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
if __name__ == "__main__":
    unittest.main()