
import unittest
import numpy

import common.utilities
import data.generator
import metrics.ordinary_differential
import metrics.statistical_tests
import models.model_data
import results.plot
import solvers.initial_value
import solvers.least_squares
import solvers.plot


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    dx_dt = p * u - x
    return dx_dt


class RunLinearOdeExperiments(unittest.TestCase):

    def do_setup(self):
        final_time = 3.0
        intervals = 30
        stdev = 0.2
        
        ref_model_instance = dict(models.model_data.model_structure)
        ref_model_instance["parameters"] = numpy.array([1.0, 2.0])
        ref_model_instance["inputs"] = numpy.array([1.0, 2.0])
        ref_model_instance["states"] = numpy.array([10.0, 8.0])
        ref_model_instance["time"] = 0.0
        
        ref_problem_instance = dict(models.model_data.problem_structure)
        ref_problem_instance["initial_conditions"] = numpy.array([10.0, 8.0])
        ref_problem_instance["time"] = numpy.arange(0.0, final_time, final_time / intervals)
        ref_problem_instance["parameters"] = numpy.array([1.0, 2.0])
        ref_problem_instance["parameter_indices"] = numpy.array([0, 1])
        ref_problem_instance["inputs"] = numpy.array([1.0, 2.0])

        measured = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            linear_2p2s_mock, ref_model_instance, ref_problem_instance))
        
        true_measurement_trajectories = common.utilities.sliceit_astrajectory(measured)
        
        measurement_noise = numpy.zeros([2,intervals])
        data.generator.set_seed(117)
        measurement_noise[0] = stdev * data.generator.normal_distribution(intervals)
        measurement_noise[1] = stdev * data.generator.normal_distribution(intervals)
        data.generator.unset_seed()
        
        experimental_measurement_trajectories = true_measurement_trajectories + measurement_noise
        
        problem_instance = dict(ref_problem_instance)
        problem_instance["outputs"] = experimental_measurement_trajectories
        problem_instance["output_indices"] = [0, 1]

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = problem_instance["parameters"]
        model_instance["inputs"] = problem_instance["inputs"]
        model_instance["states"] = problem_instance["initial_conditions"]
        model_instance["time"] = 0.0
        
        return ref_model_instance, ref_problem_instance, model_instance, problem_instance, stdev, \
            true_measurement_trajectories, experimental_measurement_trajectories, measurement_noise


    def do_slice_data(self, ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj):
        emts = slice(0, len(exp_meas_traj[0]), 2)
        emt = []
        emt.append(exp_meas_traj[0][(emts)])
        emt.append(exp_meas_traj[1][(emts)])
        tm = ref_problem_instance["time"][emts]
        tmte = []
        tmte.append(act_meas_traj[0][(emts)])
        tmte.append(act_meas_traj[1][(emts)])
        mne = []
        mne.append(meas_noise_traj[0][emts])
        mne.append(meas_noise_traj[1][emts])
        
        evts = slice(1, len(exp_meas_traj[0]), 2)
        evt = []
        evt.append([exp_meas_traj[0][0]])
        evt[0].extend(exp_meas_traj[0][(evts)])
        evt.append([exp_meas_traj[1][0]])
        evt[1].extend(exp_meas_traj[1][(evts)])
        tv = numpy.concatenate((numpy.array([ref_problem_instance["time"][0]]), numpy.array(ref_problem_instance["time"][evts])))
        tmtv = []
        tmtv.append([act_meas_traj[0][0]])
        tmtv[0].extend(act_meas_traj[0][(evts)])
        tmtv.append([act_meas_traj[1][0]])
        tmtv[1].extend(act_meas_traj[1][(evts)])
        mnv = []
        mnv.append([meas_noise_traj[0][0]])
        mnv[0].extend(meas_noise_traj[0][evts])
        mnv.append([meas_noise_traj[1][0]])
        mnv[1].extend(meas_noise_traj[1][evts])

        return tm, emt, tmte, mne, tv, evt, tmtv, mnv  
    
    
    def do_workflow(self, model_instance, problem_instance, algorithm_instance, \
        stdev, meas_noise_traj, act_meas_traj):
        # config
        do_reporting = False
        
        # objective function
        sum_sq_res_actual = metrics.ordinary_differential.sum_squared_residuals_st( \
            problem_instance["parameters"], linear_2p2s_mock, model_instance, problem_instance)

        # objective-function contributions
        sums_sq_res_actual = metrics.ordinary_differential.sums_squared_residuals( \
            problem_instance["parameters"], linear_2p2s_mock, model_instance, problem_instance)

        # observables' trajectories
        predicted_snapshots = solvers.initial_value.compute_trajectory_st( \
            linear_2p2s_mock, model_instance, problem_instance)
        predicted_values = common.utilities.sliceit_astrajectory(predicted_snapshots)
        
        # residuals' trajectories
        residuals_values = metrics.ordinary_differential.residuals_st( \
            linear_2p2s_mock, model_instance, problem_instance)

        # global ssr test
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            problem_instance["outputs"], problem_instance["parameter_indices"])
        self.assertTrue(metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            sum_sq_res_actual / stdev **2, dof, 0.95))
        
        # observables' ssr test
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            problem_instance["outputs"][0], problem_instance["parameter_indices"])
        self.assertTrue(metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            sums_sq_res_actual[0] / stdev **2, dof, 0.95))
        self.assertTrue(metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            sums_sq_res_actual[1] / stdev **2, dof, 0.95))

        if do_reporting:
            print(problem_instance["parameters"])
            print(sum_sq_res_actual)
            print(sums_sq_res_actual)
            results.plot.plot_fit(problem_instance["time"], problem_instance["outputs"], predicted_values, act_meas_traj)
            results.plot.plot_residuals(problem_instance["time"], residuals_values)
            results.plot.plot_errors_and_residuals(problem_instance["time"], meas_noise_traj, residuals_values)
    

    def do_explore_solution_path(self, dv_path, model_instance, problem_instance, stdev):
        do_reporting = False
        
        iterations = []
        objfunc_path = []
        objfunc_contribs_path = []
        ssr_path = []
        ssr_contribs_path = []
        iter = 0
        for dvs in dv_path:
            iterations.append(iter)

            # objective function
            sum_sq_res = metrics.ordinary_differential.sum_squared_residuals_st( \
                dvs[0], linear_2p2s_mock, model_instance, problem_instance)
            # objective-function contributions
            sums_sq_res = metrics.ordinary_differential.sums_squared_residuals( \
                dvs[0], linear_2p2s_mock, model_instance, problem_instance)
            # global ssr test
            dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
                problem_instance["outputs"], problem_instance["parameter_indices"])
            test_chisquared = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
                sum_sq_res / stdev **2, dof, 0.95)
            # observables' ssr test
            dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
                problem_instance["outputs"][0], problem_instance["parameter_indices"])
            tests_chisquared = []
            tests_chisquared.append(metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
                sums_sq_res[0] / stdev **2, dof, 0.95))
            tests_chisquared.append(metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
                sums_sq_res[1] / stdev **2, dof, 0.95))
             
            objfunc_path.append(sum_sq_res)
            objfunc_contribs_path.append(sums_sq_res)
            ssr_path.append(test_chisquared)
            ssr_contribs_path.append(tests_chisquared)
            
            iter += 1

        if do_reporting:
            solvers.plot.plot_objective_function(iterations, objfunc_path)
            solvers.plot.plot_objective_function_contributions(iterations, objfunc_contribs_path)
            solvers.plot.plot_chi_squared_test(iterations, ssr_path)
            solvers.plot.plot_chi_squared_tests(iterations, ssr_contribs_path)
        

    def test_workflow_st_linear_2p2s(self):
        # configure
        do_reporting = False
        
        # setup
        ref_model_instance, ref_problem_instance, model_instance, problem_instance, \
            stdev, act_meas_traj, exp_meas_traj, meas_noise_traj = self.do_setup()

        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        logger = solvers.least_squares.DecisionVariableLogger()
        algorithm_instance["callback"] = logger.log_decision_variables
        algorithm_instance["initial_guesses"] = problem_instance["parameters"]
        algorithm_instance["method"] = 'Nelder-Mead'
        
        # whole data set
        # least-squares
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            linear_2p2s_mock, model_instance, problem_instance, algorithm_instance)
        problem_instance["parameters"] = result.x
        decision_variables = logger.get_decision_variables()

        self.do_workflow(model_instance, problem_instance, algorithm_instance, stdev, meas_noise_traj, act_meas_traj)
        self.do_explore_solution_path(decision_variables, model_instance, problem_instance, stdev)
        
        # slicing data
        tm, emt, tmte, mne, tv, evt, tmtv, mnv = self.do_slice_data(ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj)

        # calibration data set
        # least-squares
        logger = solvers.least_squares.DecisionVariableLogger()
        algorithm_instance["callback"] = logger.log_decision_variables
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            linear_2p2s_mock, model_instance, problem_instance, algorithm_instance)
        problem_instance["parameters"] = result.x
        decision_variables = logger.get_decision_variables()
        
        problem_instance["outputs"] = emt
        problem_instance["time"] = tm
        self.do_workflow(model_instance, problem_instance, algorithm_instance, stdev, mne, tmte)

        # validation data set
        problem_instance["outputs"] = evt
        problem_instance["time"] = tv
        self.do_workflow(model_instance, problem_instance, algorithm_instance, stdev, mnv, tmtv)
       
        self.assertTrue(True)


    def test_montecarlo_st_linear_2p2s(self):
        # configure
        do_reporting = False
        
        # setup
        rmi, rpi, mi, pi, \
            stdev, act_meas_traj, exp_meas_traj, meas_noise_traj = self.do_setup()
        
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
        if do_reporting:
            results.plot.plot_observation_ensembles(pi["time"], mc_outputs)
            results.plot.plot_observation_ensembles(pi["time"], mc_residuals)
            import matplotlib.pyplot as pp
            pp.plot(pairs[0], pairs[1], 'ro')
            pp.show()
        
        self.assertTrue(True)
        
                
if __name__ == "__main__":
    unittest.main()
#    suite = unittest.TestSuite()
#    suite.addTest(RunLinearOdeExperiments("test_montecarlo_st_linear_2p2s"))
#    runner = unittest.TextTestRunner()
#    runner.run(suite)
