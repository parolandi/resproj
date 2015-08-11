
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
import common.environment as coen
import workflows.experiments as woex
import workflows.reporting_unlegacy as wore


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
Splicing yes-yes-no
Calibration
See also: exp-22
'''
class TestExperiment16(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment16, self).__init__(*args, **kwargs)
        self.do_plotting = coen.get_doing_plotting()
        self.do_quick_tests_only = coen.get_doing_quick_tests_only()
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-16: start")
        logging.info(codi.get_date_and_time())


    def __del__(self):
        logging.info("exp-16: finish")
        logging.info(codi.get_date_and_time())

    
    def test_calibration_workflow(self):
        logging.debug("experiments.experiment_15.test_calibration_workflow")
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 91.42486076854522
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.09002587e-05,   6.01415123e+06,   7.70693208e-03, 1.85838333e-01])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-01])

        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesyesno
        calibrated = woex.test_baseline_calibration(experiment, basepoint, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
    def test_calibration_and_validation(self):
        logging.debug("experiments.experiment_15.test_calibration_and_validation")
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 91.42486076854522
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.09002587e-05,   6.01415123e+06,   7.70693208e-03, 1.85838333e-01])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-01])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 181.34162033753552
        
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesyesno
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)

    
    def test_calibration_and_validation_global(self):
        logging.debug("experiments.experiment_15.test_calibration_and_validation_global")
        if self.do_quick_tests_only:
            return
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 91.4248295011284
        basepoint["point"]["decision_variables"] = numpy.array( \
            [  7.08951868e-05,   6.01434666e+06,   7.70847783e-03, 1.85468424e-01])
        basepoint["of_delta"] = 0.000000001
        basepoint["dv_deltas"] = numpy.array( \
            [  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-01])
        basepoint = baseline["valid"]
        basepoint["point"]["objective_function"] = 181.34776433392548
        
        experiment = sekrbi.do_experiment_setup_0_60_spliced_yesyesno_with_global_neldermead_100_10xpm
        calibrated = woex.test_baseline_calibration_and_validation(experiment, baseline, self)
        if self.do_plotting:
            wore.plot_tiled_calibration_and_validation_trajectories_at_point(experiment(), calibrated)


if __name__ == "__main__":
    unittest.main()
