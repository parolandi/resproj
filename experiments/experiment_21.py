
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
yes-no-yes splicing
'''

# WIP: 2015-06-28; extract from exp-14
class TestExperiment21(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment21, self).__init__(*args, **kwargs)
        self.do_plotting = True
        self.do_quick_tests_only = False
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-21")
        logging.info(codi.get_date_and_time())


    def test_nonlinear_confidence_region(self):
        if self.do_quick_tests_only:
            return
        baseline = {}
        baseline["point"] = {}
        baseline["point"]["objective_function"] = 191.9159661
        baseline["point"]["decision_variables"] = numpy.array( \
            [  7.21144459e-05,  5.92826673e+06,  1.21249611e-02,  1.71735070e-02])
        # WIP; more than 1? how many required for full characterisation?
        baseline["number_of_points"] = 1
        baseline["intervals"] = [ \
            [4.721085304328252e-05, 0.00014639408975853561], \
            [5999537.6911295187, 10015366.695155494], \
            [0.0030218129834986489, 1.742703135385864], \
            [0.00041379366926754218, 2.0432561489154017]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "Exp-17: NCR benchmark model (95%)"
        
        experiment = sekrbi.do_experiment_protocol_setup_0_60_yesnoyes_ncr
        woex.test_calibration_with_nonlinear_confidence_region(experiment(), baseline, self)


if __name__ == "__main__":
    unittest.main()