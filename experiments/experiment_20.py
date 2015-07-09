
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
import results.plot_data as replda
import workflows.experiments as woex


'''
Kremling bioreactor
Calculate and test nonlinear confidence region at low/high confidence
Calculate and test approximate linear confidence region at low/high confidence
0-60 hr interval
'''

# WIP: 2015-06-28; extract from exp-14
class TestExperiment20(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment20, self).__init__(*args, **kwargs)
        self.do_plotting = True
        self.do_quick_tests_only = False
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-20")
        logging.info(codi.get_date_and_time())


    def test_nonlinear_confidence_region(self):
        if self.do_quick_tests_only:
            return
        baseline = {}
        baseline["point"] = {}
        baseline["point"]["objective_function"] = 191.9159661
        baseline["point"]["decision_variables"] = numpy.array( \
            [  7.212144459e-05,  5.92826673e+06,  1.21249611e-02,  1.71735070e-02])
        # WIP; more than 1? how many required for full characterisation?
        baseline["number_of_points"] = 0
        baseline["intervals"] = [ \
            [7.1658496326300477e-05, 7.4404418807739317e-05], \
            [5999999.0032838425, 6659493.2891191998], \
            [0.0079139594140585634, 0.16454952777015888], \
            [0.0011241165870377707, 0.093956469210582788]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model (95%)"
        woex.test_calibration_with_nonlinear_confidence_region( \
            sekrbi.do_experiment_protocol_setup_0_60_calib_ncr(), baseline, self)


if __name__ == "__main__":
    unittest.main()