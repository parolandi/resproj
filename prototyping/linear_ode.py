
import unittest
import math
import numpy

import common.utilities
import data.generator
import metrics.ordinary_differential
import models.model_data
import results.plot
import solvers.initial_value
import solvers.least_squares
import metrics.statistical_tests

def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    dx_dt = p * u - x
    return dx_dt


class RunLinearOdeExperiments(unittest.TestCase):

    def do_setup(self):
        ref_model_instance = dict(models.model_data.model_structure)
        ref_model_instance["parameters"] = numpy.array([1.0, 2.0])
        ref_model_instance["inputs"] = numpy.array([1.0, 2.0])
        ref_model_instance["states"] = numpy.array([10.0, 8.0])
        ref_model_instance["time"] = 0.0
        
        ref_problem_instance = dict(models.model_data.problem_structure)
        ref_problem_instance["initial_conditions"] = numpy.array([10.0, 8.0])
        final_time = 3.0
        intervals = 30
        ref_problem_instance["time"] = numpy.arange(0.0, final_time, final_time / intervals)
        ref_problem_instance["parameters"] = numpy.array([1.0, 2.0])
        ref_problem_instance["parameter_indices"] = numpy.array([0, 1])
        ref_problem_instance["inputs"] = numpy.array([1.0, 2.0])

        measured = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            linear_2p2s_mock, ref_model_instance, ref_problem_instance))
        true_measurement_trajectories = common.utilities.sliceit_astrajectory(measured)
#        results.plot_legacy.plotobservations(ref_problem_instance["time"], true_measurement_trajectories)
        measurement_noise = numpy.zeros([2,intervals])
        data.generator.set_seed(117)
        stdev = 0.2
        measurement_noise[0] = stdev * data.generator.normal_distribution(intervals)
        measurement_noise[1] = stdev * data.generator.normal_distribution(intervals)
#        print("cov-matrix", numpy.cov(measurement_noise[0], measurement_noise[1]))
#        print("corr-matrix", numpy.corrcoef(measurement_noise[0], measurement_noise[1]))
#        results.plot_legacy.plotobservations(ref_problem_instance["time"], measurement_noise)
        data.generator.unset_seed()
        experimental_measurement_trajectories = true_measurement_trajectories + measurement_noise
#        results.plot_legacy.plotobservations(ref_problem_instance["time"], experimental_measurement_trajectories)
        
        problem_instance = dict(ref_problem_instance)
        '''
        problem_instance["initial_conditions"] = numpy.array([0.0, 1.0])
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = numpy.array([0.1, 10])
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["inputs"] = numpy.array([1.0, 2.0])
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]
        '''
        problem_instance["outputs"] = experimental_measurement_trajectories
        problem_instance["output_indices"] = [0, 1]

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0
        return ref_model_instance, ref_problem_instance, model_instance, problem_instance


    def test_solve_st_linear_2p2s(self):
        ref_model_instance = dict(models.model_data.model_structure)
        ref_model_instance["parameters"] = numpy.array([1.0, 2.0])
        ref_model_instance["inputs"] = numpy.array([1.0, 2.0])
        ref_model_instance["states"] = numpy.array([10.0, 8.0])
        ref_model_instance["time"] = 0.0
        
        ref_problem_instance = dict(models.model_data.problem_structure)
        ref_problem_instance["initial_conditions"] = numpy.array([10.0, 8.0])
        final_time = 3.0
        intervals = 30
        ref_problem_instance["time"] = numpy.arange(0.0, final_time, final_time / intervals)
        ref_problem_instance["parameters"] = numpy.array([1.0, 2.0])
        ref_problem_instance["parameter_indices"] = numpy.array([0, 1])
        ref_problem_instance["inputs"] = numpy.array([1.0, 2.0])

        measured = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            linear_2p2s_mock, ref_model_instance, ref_problem_instance))
        true_measurement_trajectories = common.utilities.sliceit_astrajectory(measured)
#        results.plot_legacy.plotobservations(ref_problem_instance["time"], true_measurement_trajectories)
        measurement_noise = numpy.zeros([2,intervals])
        data.generator.set_seed(117)
        stdev = 0.2
        measurement_noise[0] = stdev * data.generator.normal_distribution(intervals)
        measurement_noise[1] = stdev * data.generator.normal_distribution(intervals)
#        print("cov-matrix", numpy.cov(measurement_noise[0], measurement_noise[1]))
#        print("corr-matrix", numpy.corrcoef(measurement_noise[0], measurement_noise[1]))
#        results.plot_legacy.plotobservations(ref_problem_instance["time"], measurement_noise)
        data.generator.unset_seed()
        experimental_measurement_trajectories = true_measurement_trajectories + measurement_noise
#        results.plot_legacy.plotobservations(ref_problem_instance["time"], experimental_measurement_trajectories)
        
        problem_instance = dict(ref_problem_instance)
        '''
        problem_instance["initial_conditions"] = numpy.array([0.0, 1.0])
        problem_instance["time"] = numpy.arange(0.0, 1.0, 1.0 / 10)
        problem_instance["parameters"] = numpy.array([0.1, 10])
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["inputs"] = numpy.array([1.0, 2.0])
        problem_instance["outputs"] = measured
        problem_instance["output_indices"] = [0, 1]
        '''
        problem_instance["outputs"] = experimental_measurement_trajectories
        problem_instance["output_indices"] = [0, 1]

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0

        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        algorithm_instance["method"] = 'SLSQP'
        algorithm_instance["initial_guesses"] = problem_instance["parameters"]
        
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            linear_2p2s_mock, model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = numpy.array([1.0, 2.0])
        print(estimate_actual)
#        [self.assertAlmostEqual(exp, act, 1) for exp, act in zip(estimate_expected, estimate_actual)]
        
        sum_sq_res_actual = metrics.ordinary_differential.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        sum_sq_res_expected = 0.0
        print(sum_sq_res_actual)
#        self.assertAlmostEqual(sum_sq_res_expected, sum_sq_res_actual, 1)
        
        problem_instance["parameters"] = estimate_actual
        predicted_snapshots = solvers.initial_value.compute_trajectory_st( \
            linear_2p2s_mock, model_instance, problem_instance)
        predicted_values = common.utilities.sliceit_astrajectory(predicted_snapshots)
         
        results.plot.plot_fit(ref_problem_instance["time"], \
            experimental_measurement_trajectories, predicted_values, true_measurement_trajectories)

        residuals_values = metrics.ordinary_differential.residuals_st( \
            linear_2p2s_mock, model_instance, problem_instance)
        
        results.plot.plot_residuals(ref_problem_instance["time"], residuals_values)
        
        results.plot.plot_errors_and_residuals(ref_problem_instance["time"], measurement_noise, residuals_values)

        ssr = metrics.ordinary_differential.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        scaled_ssr = ssr / stdev **2
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            experimental_measurement_trajectories, ref_problem_instance["parameter_indices"])
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_ssr, dof, 0.95)
        
        scaled_residuals = metrics.ordinary_differential.sums_squared_residuals( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            experimental_measurement_trajectories[0], ref_problem_instance["parameter_indices"])
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_residuals[0] / stdev **2, dof, 0.95)
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_residuals[1] / stdev **2, dof, 0.95)

        emts = slice(0, len(experimental_measurement_trajectories[0]), 2)
        emt = []
        emt.append(experimental_measurement_trajectories[0][(emts)])
        emt.append(experimental_measurement_trajectories[1][(emts)])
        tm = ref_problem_instance["time"][emts]
        tmte = []
        tmte.append(true_measurement_trajectories[0][(emts)])
        tmte.append(true_measurement_trajectories[1][(emts)])
        mne = []
        mne.append(measurement_noise[0][emts])
        mne.append(measurement_noise[1][emts])
        
        evts = slice(1, len(experimental_measurement_trajectories[0]), 2)
        evt = []
        evt.append([experimental_measurement_trajectories[0][0]])
        evt[0].extend(experimental_measurement_trajectories[0][(evts)])
        evt.append([experimental_measurement_trajectories[1][0]])
        evt[1].extend(experimental_measurement_trajectories[1][(evts)])
        print(numpy.array([ref_problem_instance["time"][0]]))
        print(numpy.array(ref_problem_instance["time"][evts]))
        tv = numpy.concatenate((numpy.array([ref_problem_instance["time"][0]]), numpy.array(ref_problem_instance["time"][evts])))
        tmtv = []
        tmtv.append([true_measurement_trajectories[0][0]])
        tmtv[0].extend(true_measurement_trajectories[0][(evts)])
        tmtv.append([true_measurement_trajectories[1][0]])
        tmtv[1].extend(true_measurement_trajectories[1][(evts)])
        mnv = []
        mnv.append([measurement_noise[0][0]])
        mnv[0].extend(measurement_noise[0][evts])
        mnv.append([measurement_noise[1][0]])
        mnv[1].extend(measurement_noise[1][evts])
        '''
        print(tm)
        print(tv)
        print(emt)
        print(evt)
        '''
        problem_instance["outputs"] = emt
        problem_instance["time"] = tm
        
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            linear_2p2s_mock, model_instance, problem_instance, algorithm_instance)
        estimate_actual = result.x
        estimate_expected = numpy.array([1.0, 2.0])
        print(estimate_actual)
        #TODO: compute distance
        
        problem_instance["parameters"] = estimate_actual
        predicted_snapshots = solvers.initial_value.compute_trajectory_st( \
            linear_2p2s_mock, model_instance, problem_instance)
        predicted_values = common.utilities.sliceit_astrajectory(predicted_snapshots)
         
        results.plot.plot_fit(tm, \
            emt, predicted_values, tmte)

        residuals_values = metrics.ordinary_differential.residuals_st( \
            linear_2p2s_mock, model_instance, problem_instance)
        
        results.plot.plot_residuals(tm, residuals_values)
        
        results.plot.plot_errors_and_residuals(tm, mne, residuals_values)
        
        ssr = metrics.ordinary_differential.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        scaled_ssr = ssr / stdev **2
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            emt, ref_problem_instance["parameter_indices"])
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_ssr, dof, 0.95)
        
        scaled_residuals = metrics.ordinary_differential.sums_squared_residuals( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            emt[0], ref_problem_instance["parameter_indices"])
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_residuals[0] / stdev **2, dof, 0.95)
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_residuals[1] / stdev **2, dof, 0.95)

        problem_instance["outputs"] = evt
        problem_instance["time"] = tv

        problem_instance["parameters"] = estimate_actual
        validation_snapshots = solvers.initial_value.compute_trajectory_st( \
            linear_2p2s_mock, model_instance, problem_instance)
        validation_values = common.utilities.sliceit_astrajectory(validation_snapshots)
         
        print(len(tv))
        print(len(evt[0]))
        print(len(validation_values[0]))
        print(len(tmtv))
        results.plot.plot_fit(tv, \
            evt, validation_values, tmtv)

        residuals_values = metrics.ordinary_differential.residuals_st( \
            linear_2p2s_mock, model_instance, problem_instance)
        
        results.plot.plot_residuals(tv, residuals_values)
        
        results.plot.plot_errors_and_residuals(tv, mnv, residuals_values)
        
        ssr = metrics.ordinary_differential.sum_squared_residuals_st( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        scaled_ssr = ssr / stdev **2
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            evt, ref_problem_instance["parameter_indices"])
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_ssr, dof, 0.95)
        
        scaled_residuals = metrics.ordinary_differential.sums_squared_residuals( \
            estimate_actual, linear_2p2s_mock, model_instance, problem_instance)
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            evt[0], ref_problem_instance["parameter_indices"])
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_residuals[0] / stdev **2, dof, 0.95)
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            scaled_residuals[1] / stdev **2, dof, 0.95)


    def test_montecarlo_st_linear_2p2s(self):
        rmi, rpi, mi, pi = self.do_setup()
        
        stdev = 0.25
        NS = 20
        mc_inputs = numpy.vstack(( \
            numpy.asarray(rmi["parameters"][0] * (1+stdev*2*(numpy.random.sample(NS)-0.5))),
            numpy.asarray(rmi["parameters"][1] * (1+stdev*2*(numpy.random.sample(NS)-0.5)))))
        mct = numpy.transpose(mc_inputs)

        mc_outputs = []
        mc_residuals = []
        sums_mc_residuals = []
        for ii in range(len(mct)):
            pi["parameters"] = mct[ii]
            snapshots = solvers.initial_value.compute_trajectory_st(linear_2p2s_mock, mi, pi)
            trajectories = common.utilities.sliceit_astrajectory(snapshots)
            mc_outputs.append(trajectories)
            residuals = metrics.ordinary_differential.residuals_st(linear_2p2s_mock, mi, pi)
            mc_residuals.append(residuals)
            sums = metrics.ordinary_differential.sums_squared_residuals(mct[ii], linear_2p2s_mock, mi, pi)
            sums_mc_residuals.append(sums)

        pairs = numpy.transpose(sums_mc_residuals)
        print(pairs)
        results.plot.plot_observation_ensembles(pi["time"], mc_outputs)
        results.plot.plot_observation_ensembles(pi["time"], mc_residuals)
        import matplotlib.pyplot as pp
        pp.plot(pairs[0], pairs[1], 'ro')
        pp.show()
        
        
        self.assertTrue(True)
        
                
if __name__ == "__main__":
#    unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(RunLinearOdeExperiments("test_montecarlo_st_linear_2p2s"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
