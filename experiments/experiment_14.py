
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging
import numpy

import common.diagnostics as codi
import engine.confidence_regions as ecr
import results.plot_combinatorial as replco
import results.plot_data as replda
import workflows.experiments as woex
import workflows.protocols as wopr


'''
Kremling bioreactor
Calculate and test nonlinear confidence region at low/high confidence
Calculate and test approximate linear confidence region at low/high confidence
'''
class TestExperiment14(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment14, self).__init__(*args, **kwargs)
        self.do_plotting = False
        self.do_quick_tests_only = True
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())

    
    def do_experiment_setup(self):
        config = sekrbi.do_experiment_setup()
        config["algorithm_setup"] = sekrbi.do_algorithm_setup_using_slsqp_with_positivity
        return config


    def do_experiment_setup_with_low_confidence(self):
        config = self.do_experiment_setup()
        config["problem_setup"] = sekrbi.do_problem_setup_with_covariance_2_and_low_confidence
        return config

    
    def do_test_compute_linearised_confidence_region(self, config, baseline):
        best_point = wopr.do_calibration_and_compute_performance_measure(config)
        
        # setup lin conf reg
        intervals = ecr.compute_linearised_confidence_intervals(config, best_point)
        expected = baseline["intervals"]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(numpy.asarray(intervals).flatten(), numpy.asarray(expected).flatten())]
        ellipsoid = ecr.compute_linearised_confidence_region_ellipsoid(config, best_point)
        expected = baseline["ellipsoid"]
        diff = baseline["delta"]
        [self.assertAlmostEquals(act, exp, delta=eps) for act, exp, eps in zip( \
            numpy.asarray(ellipsoid).flatten(), numpy.asarray(expected).flatten(), numpy.asarray(diff).flatten())]
        
        if self.do_plotting:
            replco.plot_combinatorial_ellipsoid_projections(best_point['decision_variables'], ellipsoid)        


    def test_ncr(self):
        if self.do_quick_tests_only:
            return
        baseline = {}
        baseline["number_of_points"] = 80
        baseline["intervals"] = [ \
            [1.8560953554168591e-05, 0.00028858598850377325], \
            [5999621.511495593, 311185069.71460104], \
            [0.00063242352072096094, 0.040354449881673735], \
            [0.0062924327562778317, 62.924327562777854]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model (95%)"
        woex.test_calibration_with_nonlinear_confidence_region( \
            sekrbi.do_experiment_protocol_setup_0_20_calib_ncr(), baseline, self)

     
    def test_ncr_low_confidence(self):
        if self.do_quick_tests_only:
            return
        baseline = {}
        baseline["number_of_points"] = 81
        baseline["intervals"] = [ \
            [1.9918149990245181e-05, 0.00027202677048785735], \
            [5999903.1790274335, 6000588.7692325944], \
            [0.00070910862594929702, 0.037986101795423888], \
            [0.0062924327298415237, 62.924327562777854]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model (25%)"
        woex.test_calibration_with_nonlinear_confidence_region( \
            sekrbi.do_experiment_protocol_setup_0_20_calib_ncr_low_confidence(), baseline, self)


    def test_lcr(self):
        baseline = {}
        baseline["intervals"] = [ \
            [4.9423053215497172e-05, 0.00026694444088288676], \
            [-113597360.94805983, 125597359.64413485], \
            [-0.26987827573815093, 0.33646951374979961], \
            [-513.87991160491765, 515.13839815617325]]
        baseline["ellipsoid"] = [ \
            [  6.12718097e-06, -1.09502057e+05,  8.69533106e-04, -2.02686196e+00], \
            [ -1.09502057e+05,  7.40900618e+18,  5.94586975e+08, -8.05367692e+12], \
            [  8.69533106e-04,  5.94586975e+08,  4.76102404e+01, -6.33519915e+04], \
            [ -2.02686196e+00, -8.05367692e+12, -6.33519915e+04,  1.37120687e+08]]
        baseline["delta"] = [ \
            [  0.00000001e-06,  0.00000001e+05,  0.00000001e-04,  0.00000001e+00], \
            [  0.00000001e+05,  0.00000001e+18,  0.00000001e+08,  0.00000001e+12], \
            [  0.00000001e-04,  0.00000001e+08,  0.00000001e+01,  0.00000001e+04], \
            [  0.00000001e+00,  0.00000001e+12,  0.00000001e+04,  0.00000001e+08]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR benchmark model (95%)"
        self.do_test_compute_linearised_confidence_region(self.do_experiment_setup(), baseline)


    def test_lcr_low_confidence(self):
        baseline = {}
        baseline["intervals"] = [ \
            [0.00014082795520386246, 0.00017553953889452146], \
            [-13085083.850529518, 25085082.546604555], \
            [-0.015084203011126875, 0.081675441022775491], \
            [-81.474993833023916, 82.733480384279488]]
        baseline["ellipsoid"] = [ \
            [  1.15263027e-06, -2.05992587e+04,  1.63574438e-04, -3.81288306e-01], \
            [ -2.05992587e+04,  1.39376409e+18,  1.11852245e+08, -1.51503797e+12], \
            [  1.63574438e-04,  1.11852245e+08,  8.95632179e+00, -1.19176214e+04], \
            [ -3.81288306e-01, -1.51503797e+12, -1.19176214e+04,  2.57948078e+07]]
        baseline["delta"] = [ \
            [  0.00000001e-06,  0.00000001e+04,  0.00000001e-04,  0.00000001e-01], \
            [  0.00000001e+04,  0.00000001e+18,  0.00000001e+08,  0.00000001e+12], \
            [  0.00000001e-04,  0.00000001e+08,  0.00000001e+00,  0.00000001e+04], \
            [  0.00000001e-01,  0.00000001e+12,  0.00000001e+04,  0.00000001e+07]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR benchmark model (25%)"
        self.do_test_compute_linearised_confidence_region(self.do_experiment_setup_with_low_confidence(), baseline)


if __name__ == "__main__":
    unittest.main()
