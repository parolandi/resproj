
import unittest
import models.kremlingetal_bioreactor as testme
import setups.kremlingetal_bioreactor as testmetoo

import copy
import math
import numpy

import models.model_data
import solvers.initial_value

import common.diagnostics as cd
import common.utilities as cu
import engine.estimation_matrices
import engine.statistical_inference
import solvers.initial_value as siv
import solvers.local_sensitivities as sls
import results.plot_tiles as rpt
import models.model_data_utils as mmdu


class TestKremlingEtAlBioreactor(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestKremlingEtAlBioreactor, self).__init__(*args, **kwargs)
        self.do_plotting = False
        self.do_diag = False

    
    def test_regression(self):
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
        no_meas = cu.size_it(problem_instance["outputs"])
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
        est_stdev = engine.statistical_inference.compute_measurements_standard_deviation( \
            ssr, no_params, no_meas)
        ell_radius = engine.statistical_inference.compute_confidence_ellipsoid_radius( \
            no_params, no_meas, est_stdev, 0.9)
        confidence_intervals = engine.statistical_inference.compute_confidence_intervals( \
            cov_matrix, ell_radius)
        det = engine.estimation_matrices.calculate_determinant(cov_matrix)
        expected = [1.68587487e-14, 1.67506860e+10, 4.22215529e-06, 7.14130399e-06]
        delta = [0.00000001e-14, 0.00000001e+10, 0.00000001e-06, 0.00000001e-06]
        [self.assertAlmostEquals(act, exp, delta=dif) for act, exp, dif in zip(confidence_intervals, expected, delta)] 
        if self.do_diag:
            cd.print_maximum_sensitivities(sens_max)
            cd.print_measurements_stdev_and_ellipsoid_radius(no_meas, est_stdev, ell_radius)
            cd.print_covariance_matrix_and_determinant(cov_matrix, det)
            cd.print_decision_variables_and_confidence_intervals(problem_instance["parameters"], confidence_intervals)

    
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
    
    
if __name__ == "__main__":
    unittest.main()
