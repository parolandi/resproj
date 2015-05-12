
import unittest
import models.kremlingetal_bioreactor as testme
import setups.kremlingetal_bioreactor as testmetoo

import copy
import logging
import math
import numpy

import models.model_data
import solvers.initial_value

import common.diagnostics as codi
import common.utilities as cu
import metrics.statistical_tests as mestte
import models.model_data_utils as mmdu
import engine.estimation_matrices
import engine.statistical_inference
import results.plot_tiles as rpt
import results.plot_data as replda
import solvers.initial_value as siv
import solvers.local_sensitivities as sls
import workflows.experiments as woex
import workflows.reporting as wore


class TestKremlingEtAlBioreactor(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestKremlingEtAlBioreactor, self).__init__(*args, **kwargs)
        self.do_plotting = False
        self.do_diag = False
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())

    
    def test_simulation_regression(self):
        t = numpy.linspace(0.0, 20.0, 11)
        p = numpy.ones(len(testme.pmap))
        for par in testme.pmap.items():
            p[par[1]] = testme.pvec[par[0]]
        u = numpy.ones(len(testme.umap))
        for inp in testme.umap.items():
            u[inp[1]] = testme.uvec_0h[inp[0]]
        x = numpy.ones(len(testme.xmap))
        for ste in testme.xmap.items():
            x[ste[1]] = testme.xvec[ste[0]]

        model_data = dict(models.model_data.model_structure)
        model_data["parameters"] = copy.deepcopy(p)
        model_data["inputs"] = copy.deepcopy(u)
        model_data["states"] = copy.deepcopy(x)
        problem_data = dict(models.model_data.problem_structure)
        problem_data["initial_conditions"] = copy.deepcopy(x)
        problem_data["time"] = t
        problem_data["parameters"] = copy.deepcopy(p)
        problem_data["inputs"] = copy.deepcopy(u)

        trajectories = solvers.initial_value.compute_timecourse_trajectories( \
            testme.evaluate_modelB, model_data, problem_data)
        
        snapshots = solvers.initial_value.compute_trajectory_st( \
            testme.evaluate_modelB, model_data, problem_data)

        self.assertEqual(len(t), 11)
        
        # trajectory testing
        actual = trajectories[1]
        expected = numpy.asarray([0.1        , 0.45231151, 0.43154884, 0.41647925, 0.40731195, 0.40174070, \
            0.39835725, 0.39630344, 0.39505712, 0.39430094, 0.39384223])
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        actual = trajectories[2]
        expected = numpy.asarray([2.         , 0.08479020, 0.06961922, 0.07252712, 0.07442350, 0.07562755, \
            0.07637892, 0.07684270, 0.07712704, 0.07730064, 0.07740635])
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        actual = trajectories[3]
        expected = numpy.asarray([ 0.07      , 0.60392434, 0.31318971, 0.2658407,  0.2481972,  0.24128745, \
            0.23888458, 0.23841957, 0.23872791, 0.23927449, 0.23982609])
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        actual = trajectories[4]
        expected = numpy.asarray( [ 0.01     ,  0.01285411, 0.01086171, 0.01125204, 0.01150427, 0.01166346, \
            0.01176243, 0.01182338, 0.0118607,  0.01188346, 0.01189731])
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        actual = trajectories[5]
        expected = numpy.asarray([ 0.07      , 0.0136086,  0.02167494, 0.02635199, 0.02881638, 0.03003462, \
            0.03058795, 0.03080508, 0.03086304, 0.03085291, 0.03081916])
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]

        # snapshot testing        
        actual = snapshots[0]
        expected = copy.deepcopy(x)
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        actual = snapshots[len(t)-1]
        expected = numpy.asarray([ 1.        , 0.39384222, 0.07740635, 0.23982609, 0.01189731, 0.03081916])
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        
    
    def test_states_and_sensitivites_numerical(self):
        model_instance = testmetoo.do_model_setup_model_B()
        data_instance = testmetoo.do_get_published_data_spliced_111111()
        problem_instance = testmetoo.do_problem_setup(model_instance, data_instance["calib"])
        states_and_sens = sls.compute_timecourse_trajectories_and_sensitivities(model_instance, problem_instance)
        actual = [math.fsum(states_and_sens[6+ii]) for ii in range(len(states_and_sens[6:]))]
        expected = [0.0, 0.0, 0.0, 0.0, 59161.484880419586, 3.1968127959617714e-10, 0.10483539730765658, -0.06504013050356859, -14582.394274657654, -7.946087098494498e-11, 0.27708034734013914, 0.12597806783865015, -66407.97295549244, -4.884389744774786e-07, -135.78004088834632, -126.76588971721745, -1909.0309723004566, -9.464186176653491e-12, 0.03544330615211961, 0.01750572201086875, 1603.970009187875, -2.0444441761630994e-10, 14.741219787364145, 13.424883852607149]
        [self.assertAlmostEqual(act, exp, 8) for act, exp in zip(actual, expected)]
        if self.do_plotting:
            states = states_and_sens[0:6]
            sens = states_and_sens[6:]
            rpt.plot_states_and_sensitivities(problem_instance["time"], states, sens, 4)
        

    def test_confidence_intervals(self):
        model_instance = testmetoo.do_model_setup_model_B()
        data_instance = testmetoo.do_get_published_data_spliced_111111()
        problem_instance = testmetoo.do_problem_setup(model_instance, data_instance["calib"])
        no_obs = len(problem_instance["outputs"])
        no_meas = mmdu.calculate_number_of_observations(problem_instance["outputs"])
        no_params = mmdu.get_number_of_decision_variables(problem_instance)
        no_timepoints = mmdu.get_number_of_time_points(problem_instance)
        ssr = 0.045095700772591826

        # sensitivities
        states_and_sens = sls.compute_timecourse_trajectories_and_sensitivities(model_instance, problem_instance)
        sens_trajectories = states_and_sens[10:]
        sens_max = cu.get_maximum_absolute_sensitivity_value(sens_trajectories, no_obs, no_params)
        
        # all this for the confidence intervals
        cov_matrix = engine.estimation_matrices.compute_covariance_matrix( \
            no_obs, no_params, no_timepoints, sens_trajectories)
        det = engine.estimation_matrices.calculate_determinant(cov_matrix)

        confidence_intervals = engine.statistical_inference.compute_confidence_intervals( \
            cov_matrix, mestte.calculate_two_sided_t_student_value(0.9, no_meas, no_params))
        # "Yxs": 7.031E-5, k2": 5.559E6, "ksynmax": 8.2E-3, "KIB": 0.166
        expected = [  8.57302147e-05,  8.54550124e+07,  1.35671412e+00,  1.76445263e+00]
        delta = [0.00000001e-05, 0.00000001e+07, 0.00000001e+00, 0.00000001e+00]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(confidence_intervals, expected, delta)] 

        est_var = engine.statistical_inference.compute_measurements_variance( \
            ssr, no_params, no_meas)
        ell_radius = engine.statistical_inference.compute_confidence_ellipsoid_radius( \
            no_params, no_meas, est_var, 0.9)

        if self.do_diag:
            codi.print_maximum_sensitivities(sens_max)
            codi.print_measurements_est_var_and_ellipsoid_radius(no_meas, est_var, ell_radius)
            codi.print_covariance_matrix_and_determinant(cov_matrix, det)
            codi.print_decision_variables_and_confidence_intervals(problem_instance["parameters"], confidence_intervals)

    
    # TODO: not being tested at the moment
    def do_not_test_states_and_sensitivites_analytical(self):
        sens_model_instance = testmetoo.do_sensitivity_model_setup()
        data_instance = testmetoo.do_get_published_data_spliced_111111()
        sens_problem_instance = testmetoo.do_sensitivity_problem_setup(sens_model_instance, data_instance["calib"])
        states_and_sens = siv.compute_timecourse_trajectories(None, sens_model_instance, sens_problem_instance)
        states = states_and_sens[0:6]
        sens = states_and_sens[6:]
        if self.do_plotting:
            rpt.plot_states_and_sensitivities(sens_problem_instance["time"], states, sens, 4)

    
    # TODO: test published data
    

    def test_calibration_workflow_1(self):
        """
        0-20hr
        """
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 55.730316319527418
        basepoint["point"]["decision_variables"] = numpy.array( \
            [7.06036656e-05, 5.95280934e+06, 7.86546429e-03, 5.61758623e-01])
        basepoint["of_delta"] = 0.0000001
        basepoint["dv_deltas"] = numpy.array([  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-01])

        calibrated = woex.test_baseline_calibration(testmetoo.do_experiment_setup_0_20, baseline["calib"], self)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(testmetoo.do_experiment_setup_0_20(), calibrated)


    def test_calibration_workflow_2(self):
        """
        0-20hr twice
        """
        baseline = dict(woex.calib_valid_baseline)
        basepoint = baseline["calib"]
        basepoint["point"]["objective_function"] = 111.46063263905484
        basepoint["point"]["decision_variables"] = numpy.array( \
            [7.06036656e-05, 5.95280934e+06, 7.86546429e-03, 5.61758623e-01])
        basepoint["of_delta"] = 0.0000001
        basepoint["dv_deltas"] = numpy.array([  0.00000001e-05,  0.00000001e+06,  0.00000001e-03,  0.00000001e-01])

        calibrated = woex.test_baseline_calibration(testmetoo.do_experiment_setup_0_20_twice, baseline["calib"], self)
        if self.do_plotting:
            wore.plot_tiled_trajectories_at_point(testmetoo.do_experiment_setup_0_20_twice(), calibrated)


    def test_nonlinear_confidence_region_1(self):
        """
        0-20hr
        high confidence
        """
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
            testmetoo.do_experiment_protocol_setup_0_20_calib_ncr(), baseline, self)


    def test_nonlinear_confidence_region_1_low_confidence(self):
        """
        0-20hr
        low confidence
        """
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
            testmetoo.do_experiment_protocol_setup_0_20_calib_ncr_low_confidence(), baseline, self)
        

    def test_nonlinear_confidence_region_2(self):
        """
        0-20hr twice
        high confidence
        """
        baseline = {}
        baseline["number_of_points"] = 79
        baseline["intervals"] = [ \
            [9.4443554952357333e-06, 0.00098451779116363056], \
            [4489764.8093958469, 175771143.75246286], \
            [7.7677934047834407e-05, 0.1382704734970987], \
            [19.060985194397745, 190609.85194134654]]
        baseline["plotdata"] = dict(replda.plot_data)
        baseline["plotdata"]["window_title"] = "NCR benchmark model (95%)"
        woex.test_calibration_with_nonlinear_confidence_region( \
            testmetoo.do_experiment_protocol_setup_0_20_2x_calib_ncr(), baseline, self)


    def test_nonlinear_confidence_region_3(self):
        """
        0-60hr
        high confidence
        """
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
            testmetoo.do_experiment_protocol_setup_0_60_calib_ncr(), baseline, self)


if __name__ == "__main__":
    unittest.main()