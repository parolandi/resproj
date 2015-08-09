
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
Splicing yes-no-yes
Calibration, calib/valid (local and global)
'''
class TestExperiment17(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment17, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-17: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-17: finish")
        logging.info(codi.get_date_and_time())


    def test_calibration_workflow(self):
        logging.debug("experiments.experiment_17.test_calibration_workflow")
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yesnoyes(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yesnoyes(basepoint)
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesnoyes
        calibrated = woex.test_baseline_calibration(experiment, basepoint, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)


    def test_calibration_and_validation(self):
        logging.debug("experiments.experiment_17.test_calibration_and_validation")
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yesnoyes(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yesnoyes(basepoint)
        baseline["valid"]["point"]["objective_function"] = exba.get_baseline_point_0_60_yesnoyes()
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesnoyes
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
    def test_calibration_and_validation_global(self):
        logging.debug("experiments.experiment_17.test_calibration_and_validation_global")
        if self.do_quick_tests_only:
            return
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint = exba.set_baseline_point_0_60_yesnoyes_global(basepoint)
        basepoint = exba.set_baseline_eps_0_60_yesnoyes(basepoint)
        baseline["valid"]["point"]["objective_function"] = exba.get_baseline_point_0_60_yesnoyes_global()
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesnoyes_with_global_neldermead_100_10xpm
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)


if __name__ == "__main__":
    unittest.main()