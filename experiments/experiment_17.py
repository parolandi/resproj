
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
#import results.plot_data as replda
import workflows.experiments as woex
import workflows.reporting_unlegacy as wore


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
Splicing yes-no-yes
Calibration, calib/valid (local and global)
Nonlinear confidence region
'''
class TestExperiment17(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment17, self).__init__(*args, **kwargs)
        self.do_plotting = False
        self.do_quick_tests_only = True
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-17")
        logging.info(codi.get_date_and_time())

    
    def test_calibration_workflow(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 153.05359591605975
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.25907845138e-05, 5906545.40918, 0.0129296870173, 0.0144696117475])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])

        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesnoyes
        calibrated = woex.test_baseline_calibration(experiment, basepoint, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)


    def test_calibration_and_validation(self):
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 153.05359591605975
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.25907845138e-05, 5906545.40918, 0.0129296870173, 0.0144696117475])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 40.78092219391061
        
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesnoyes
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
    def test_calibration_and_validation_global(self):
        if self.do_quick_tests_only:
            return
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 153.05359591605975
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.25907845138e-05, 5906545.40918, 0.0129296870173, 0.0144696117475])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-02,  0.00000001e-02])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 40.78092219391061
        
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesnoyes_with_global_neldermead_100_10xpm
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)


if __name__ == "__main__":
    unittest.main()