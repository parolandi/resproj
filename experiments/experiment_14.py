
import unittest
import setups.kremlingetal_bioreactor as sekrbi

import logging

import common.diagnostics as codi
import results.plot_data as replda
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
        self.do_quick_tests_only = True
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-14")
        logging.info(codi.get_date_and_time())

    
    def do_experiment_setup(self):
        config = sekrbi.do_experiment_setup_0_20()
        config["algorithm_setup"] = sekrbi.do_algorithm_setup_using_slsqp_with_positivity
        return config


    def do_experiment_setup_with_low_confidence(self):
        config = sekrbi.do_experiment_setup_0_20()
        config["problem_setup"] = sekrbi.do_problem_setup_with_covariance_2_and_low_confidence
        return config

    
    def test_ncr(self):
        logging.debug("experiments.experiment_14.test_ncr")
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
        logging.debug("experiments.experiment_14.test_ncr_low_confidence")
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


    def dn_test_lcr(self):
        logging.debug("experiments.experiment_14.test_lcr")
        baseline = {}
        baseline["intervals"] = [ \
            [-3.3298285820135265e-05, 0.00017450561705501587], \
            [-49451538.410624318, 61357157.092140831], \
            [-0.12466235582771625, 0.14039328439852158], \
            [-239.32962521727927, 240.45314246285932]]
        baseline["ellipsoid"] = [ \
            [  2.98950610e-08, -5.02656235e+03, -1.09127528e-06,  1.47544377e-02], \
            [ -5.02656235e+03,  8.50040716e+15, -1.64934543e+07,  1.38933597e+10], \
            [ -1.09127528e-06, -1.64934543e+07,  4.86369289e-02, -7.21011214e+01], \
            [  1.47544377e-02,  1.38933597e+10, -7.21011214e+01,  1.59360739e+05]]
        baseline["delta"] = [ \
            [  0.00000001e-08,  0.00000001e+03,  0.00000001e-06,  0.00000001e-02], \
            [  0.00000001e+03,  0.00000001e+15,  0.00000001e+07,  0.00000001e+10], \
            [  0.00000001e-06,  0.00000001e+07,  0.00000001e-02,  0.00000001e+01], \
            [  0.00000001e-02,  0.00000001e+10,  0.00000001e+01,  0.00000001e+05]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR benchmark model (95%)"
        woex.test_calibration_with_linearised_confidence_region( \
            sekrbi.do_experiment_setup_0_20(), baseline, self)


    def test_lcr_low_confidence(self):
        logging.debug("experiments.experiment_14.test_lcr_low_confidence")
        baseline = {}
        baseline["intervals"] = [ \
            [5.4023221176441136e-05, 8.7184110058439464e-05], \
            [-2888494.3784842957, 14794113.060000809], \
            [-0.013283033195825902, 0.029013961766631242], \
            [-37.719579760198528, 38.843097005778588]]
        baseline["ellipsoid"] = [ \
            [  5.62378564e-09, -9.45584596e+02, -2.05288032e-07,  2.77556868e-03], \
            [ -9.45584596e+02,  1.59907577e+15, -3.10270822e+06,  2.61358480e+09], \
            [ -2.05288032e-07, -3.10270822e+06,  9.14945992e-03, -1.35634863e+01], \
            [  2.77556868e-03,  2.61358480e+09, -1.35634863e+01,  2.99785518e+04]]
        baseline["delta"] = [ \
            [  0.00000001e-09,  0.00000001e+02,  0.00000001e-07,  0.00000001e-03], \
            [  0.00000001e+02,  0.00000001e+15,  0.00000001e+06,  0.00000001e+09], \
            [  0.00000001e-07,  0.00000001e+06,  0.00000001e-03,  0.00000001e+01], \
            [  0.00000001e-03,  0.00000001e+09,  0.00000001e+01,  0.00000001e+04]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "LCR benchmark model (25%)"
        woex.test_calibration_with_linearised_confidence_region( \
            self.do_experiment_setup_with_low_confidence(), baseline, self)


if __name__ == "__main__":
    unittest.main()
