
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
import results.plot_data as replda
import workflows.experiments as woex
import workflows.reporting_unlegacy as wore


'''
Kremling bioreactor
Multi-stage experiment 0-60hr interval
Splicing yes-yes-no
Calibration
Nonlinear confidence region
'''
class TestExperiment16(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment16, self).__init__(*args, **kwargs)
        self.do_plotting = False
        self.do_quick_tests_only = True
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-16")
        logging.info(codi.get_date_and_time())

    
    def test_calibration_workflow(self):
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


    def dn_test_nonlinear_confidence_region(self):
        if self.do_quick_tests_only:
            return
        baseline = {}
        baseline["number_of_points"] = 1
        baseline["intervals"] = [ \
            [4.721085304328252e-05, 0.00014639408975853561], \
            [5999537.6911295187, 10015366.695155494], \
            [0.0030218129834986489, 1.742703135385864], \
            [0.00041379366926754218, 2.0432561489154017]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model (95%)"
        woex.test_calibration_with_nonlinear_confidence_region( \
            sekrbi.do_experiment_protocol_setup_0_60_calib_ncr(), baseline, self)


if __name__ == "__main__":
    unittest.main()