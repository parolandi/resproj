
import copy
import unittest
import numpy
import math
import matplotlib.pyplot

import models.ordinary_differential

import common.utilities
import data.generator
import metrics.ordinary_differential
import metrics.statistical_tests
import models.model_data
import prototyping.statistical_inference
import engine.estimation_matrices
import results.plot
import results.report_workflows
import solvers.initial_value
import solvers.least_squares
import solvers.plot
import solvers.solver_data

   
class RunLinearOdeExperiments(unittest.TestCase):

    def test_sensitivities_linear_2p2s(self):
        final_time = 2.0
        intervals = 2
        stdev = 0.2
        times = numpy.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
#        times = numpy.array([0.0, 1.0])

        sens_model_instance = dict(models.model_data.model_structure)
        sens_model_instance["parameters"] = numpy.array([1.0, 2.0])
        sens_model_instance["inputs"] = numpy.array([1.0, 2.0])
        sens_model_instance["states"] = numpy.array([0.0, 0.0, 0.0, 0.0])
        sens_model_instance["time"] = 0.0
        
        sens_problem_instance = dict(models.model_data.problem_structure)
        sens_problem_instance["initial_conditions"] = numpy.array([0.0, 0.0, 0.0, 0.0])
        sens_problem_instance["time"] = times
        sens_problem_instance["parameters"] = numpy.array([1.0, 2.0])
        sens_problem_instance["parameter_indices"] = numpy.array([0, 1])
        sens_problem_instance["inputs"] = numpy.array([1.0, 2.0])
        
        sens_snapshot = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance))
        sens_trajectories = common.utilities.sliceit_astrajectory(sens_snapshot)

        no_params = len(sens_problem_instance["parameters"])
        no_timepoints = len(sens_problem_instance["time"])
        sm = engine.estimation_matrices.prepare_sensitivity_matrix(no_params, no_timepoints, sens_trajectories)

        h = sm.transpose().dot(sm)
        print("H", h)
        varcovar = numpy.linalg.inv(h)
        print("VCM", varcovar)

        # (b-b*)^T(P)^(-1)(b-b*)=ps^2F_(1-alpha)(p,n-p)
        sys_model_instance = dict(models.model_data.model_structure)
        sys_model_instance["parameters"] = numpy.array([1.0, 2.0])
        sys_model_instance["inputs"] = numpy.array([1.0, 2.0])
        sys_model_instance["states"] = numpy.array([10.0, 8.0])
        sys_model_instance["time"] = 0.0
        
        sys_problem_instance = dict(models.model_data.problem_structure)
        sys_problem_instance["initial_conditions"] = numpy.array([10.0, 8.0])
        sys_problem_instance["time"] = times
        sys_problem_instance["parameters"] = numpy.array([1.0, 2.0])
        sys_problem_instance["parameter_indices"] = numpy.array([0, 1])
        sys_problem_instance["inputs"] = numpy.array([1.0, 2.0])

        true_snap = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            models.ordinary_differential.linear_2p2s, sys_model_instance, sys_problem_instance))
        true_traj = common.utilities.sliceit_astrajectory(true_snap)

        no_points = len(sens_problem_instance["time"])
        meas_noise = numpy.zeros([2, no_points])
        data.generator.set_seed(117)
        meas_noise[0] = stdev * data.generator.normal_distribution(no_points)
        meas_noise[1] = stdev * data.generator.normal_distribution(no_points)
        data.generator.unset_seed()

        meas_traj = true_traj + meas_noise
        sys_problem_instance["outputs"] = meas_traj
        sys_problem_instance["output_indices"] = numpy.array([0.0, 1.0])
        
        sum_sq_res_actual = metrics.ordinary_differential.sum_squared_residuals_st( \
            sys_problem_instance["parameters"], models.ordinary_differential.linear_2p2s, \
            sys_model_instance, sys_problem_instance)
        no_params = len(sys_problem_instance["parameters"])
        no_meas = no_points * 2
        est_stdev = sum_sq_res_actual / (no_meas - no_params)
        significance = 0.9
        radius = prototyping.statistical_inference.compute_confidence_ellipsoid_radius(no_params, no_meas, est_stdev, significance)
        print("radius", radius)
        r_p1 = radius * varcovar[0,0]
        r_p2 = radius * varcovar[1,1]
        print("r-p1", r_p1)
        print("r-p2", r_p2)
        
        self.assertAlmostEqual(r_p1, 0.0021714732894047291, 8)
        self.assertAlmostEqual(r_p2, 0.0005428683223511824, 8)


    def do_setup(self):
        final_time = 3.0
        intervals = 30
        stdev = 0.2
        
        times = numpy.arange(0.0, final_time, final_time / intervals)
        
        ref_model_instance = dict(models.model_data.model_structure)
        ref_model_instance["parameters"] = numpy.array([1.0, 2.0])
        ref_model_instance["inputs"] = numpy.array([1.0, 2.0])
        ref_model_instance["states"] = numpy.array([10.0, 8.0])
        ref_model_instance["time"] = 0.0
        
        ref_problem_instance = dict(models.model_data.problem_structure)
        ref_problem_instance["initial_conditions"] = numpy.array([10.0, 8.0])
        ref_problem_instance["time"] = times
        ref_problem_instance["parameters"] = numpy.array([1.0, 2.0])
        ref_problem_instance["parameter_indices"] = numpy.array([0, 1])
        ref_problem_instance["inputs"] = numpy.array([1.0, 2.0])

        measured = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            models.ordinary_differential.linear_2p2s, ref_model_instance, ref_problem_instance))
        
        true_measurement_trajectories = common.utilities.sliceit_astrajectory(measured)
        
        measurement_noise = numpy.zeros([2, intervals])
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
        
        sens_model_instance = dict(models.model_data.model_structure)
        sens_model_instance["parameters"] = numpy.array([1.0, 2.0])
        sens_model_instance["inputs"] = numpy.array([1.0, 2.0])
        sens_model_instance["states"] = numpy.array([0.0, 0.0, 0.0, 0.0])
        sens_model_instance["time"] = 0.0
        
        sens_problem_instance = dict(models.model_data.problem_structure)
        sens_problem_instance["initial_conditions"] = numpy.array([0.0, 0.0, 0.0, 0.0])
        sens_problem_instance["time"] = times
        sens_problem_instance["parameters"] = numpy.array([1.0, 2.0])
        sens_problem_instance["parameter_indices"] = numpy.array([0, 1])
        sens_problem_instance["inputs"] = numpy.array([1.0, 2.0])

        return ref_model_instance, ref_problem_instance, \
            model_instance, problem_instance, \
            sens_model_instance, sens_problem_instance, \
            stdev, true_measurement_trajectories, experimental_measurement_trajectories, measurement_noise


    def do_apply_slicing_101010_ones(self, values):
        ones = numpy.delete(values, numpy.s_[1::2])
        return ones

    
    def do_apply_slicing_1010101_zeros(self, values):
        zeros = numpy.delete(values, numpy.s_[0::2])
        return zeros


    def do_apply_slicing_110110_ones(self, values):
        ones = numpy.delete(values, numpy.s_[2::3])
        return ones

    
    def do_apply_slicing_110110_zeros(self, values):
        vals = numpy.delete(values, numpy.s_[0::3])
        zeros = numpy.delete(vals, numpy.s_[0::2])
        return zeros


    def do_slice_data_101010(self, ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj):
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
    
    
    def do_slice_data_110110(self, ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj):
        
        emt = []
        emt.append(self.do_apply_slicing_110110_ones(exp_meas_traj[0]))
        emt.append(self.do_apply_slicing_110110_ones(exp_meas_traj[1]))
        tm = self.do_apply_slicing_110110_ones(ref_problem_instance["time"])
        tmte = []
        tmte.append(self.do_apply_slicing_110110_ones(act_meas_traj[0]))
        tmte.append(self.do_apply_slicing_110110_ones(act_meas_traj[1]))
        mne = []
        mne.append(self.do_apply_slicing_110110_ones(meas_noise_traj[0]))
        mne.append(self.do_apply_slicing_110110_ones(meas_noise_traj[0]))
        
        evt = []
        evt.append([exp_meas_traj[0][0]])
        evt[0].extend(self.do_apply_slicing_110110_zeros(exp_meas_traj[0]))
        evt.append([exp_meas_traj[1][0]])
        evt[1].extend(self.do_apply_slicing_110110_zeros(exp_meas_traj[1]))
        tv = numpy.concatenate(( \
            numpy.array([ref_problem_instance["time"][0]]), \
            self.do_apply_slicing_110110_zeros(ref_problem_instance["time"]) \
            ))
        tmtv = []
        tmtv.append([act_meas_traj[0][0]])
        tmtv[0].extend(self.do_apply_slicing_110110_zeros(act_meas_traj[0]))
        tmtv.append([act_meas_traj[1][0]])
        tmtv[1].extend(self.do_apply_slicing_110110_zeros(act_meas_traj[1]))
        mnv = []
        mnv.append([meas_noise_traj[0][0]])
        mnv[0].extend(self.do_apply_slicing_110110_zeros(meas_noise_traj[0]))
        mnv.append([meas_noise_traj[1][0]])
        mnv[1].extend(self.do_apply_slicing_110110_zeros(meas_noise_traj[1]))

        return tm, emt, tmte, mne, tv, evt, tmtv, mnv  

    
    def do_slice_data_111000(self, ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj):
        half = len(exp_meas_traj[0]) // 2
        emts = slice(0, half, 1)
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
        
        evts = slice(half, len(exp_meas_traj[0]), 1)
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

    
    def do_slice_data_000111(self, ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj):
        half = len(exp_meas_traj[0]) // 2
        emts = slice(half, len(exp_meas_traj[0]), 1)
        emt = []
        emt.append([exp_meas_traj[0][0]])
        emt[0].extend(exp_meas_traj[0][emts])
        emt.append([exp_meas_traj[1][0]])
        emt[1].extend(exp_meas_traj[1][emts])
        tm = numpy.concatenate((numpy.array([ref_problem_instance["time"][0]]), numpy.array(ref_problem_instance["time"][emts])))
        tmte = []
        tmte.append([act_meas_traj[0][0]])
        tmte[0].extend(act_meas_traj[0][(emts)])
        tmte.append([act_meas_traj[1][0]])
        tmte[1].extend(act_meas_traj[1][(emts)])
        mne = []
        mne.append([meas_noise_traj[0][0]])
        mne[0].extend(meas_noise_traj[0][emts])
        mne.append([meas_noise_traj[1][0]])
        mne[1].extend(meas_noise_traj[1][emts])
        
        evts = slice(0, half, 1)
        evt = []
        evt.append(exp_meas_traj[0][(evts)])
        evt.append(exp_meas_traj[1][(evts)])
        tv = ref_problem_instance["time"][evts]
        tmtv = []
        tmtv.append(act_meas_traj[0][(evts)])
        tmtv.append(act_meas_traj[1][(evts)])
        mnv = []
        mnv.append(meas_noise_traj[0][evts])
        mnv.append(meas_noise_traj[1][evts])

        return tm, emt, tmte, mne, tv, evt, tmtv, mnv  

    
    def do_workflow(self, model_instance, problem_instance, \
        sens_model_instance, sens_problem_instance, \
        stdev, meas_noise_traj, act_meas_traj):
        # config
        do_reporting = False
        
        # objective function
        sum_sq_res_actual = metrics.ordinary_differential.sum_squared_residuals_st( \
            problem_instance["parameters"], models.ordinary_differential.linear_2p2s, \
            model_instance, problem_instance)

        # objective-function contributions
        sums_sq_res_actual = metrics.ordinary_differential.sums_squared_residuals( \
            problem_instance["parameters"], models.ordinary_differential.linear_2p2s, \
            model_instance, problem_instance)

        # observables' trajectories
        predicted_snapshots = solvers.initial_value.compute_trajectory_st( \
            models.ordinary_differential.linear_2p2s, model_instance, problem_instance)
        predicted_values = common.utilities.sliceit_astrajectory(predicted_snapshots)
        
        # residuals' trajectories
        residuals_values = metrics.ordinary_differential.residuals_st( \
            models.ordinary_differential.linear_2p2s, model_instance, problem_instance)

        # global ssr test
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            problem_instance["outputs"], problem_instance["parameter_indices"])
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            sum_sq_res_actual / stdev **2, dof, 0.95)
        
        # observables' ssr test
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            problem_instance["outputs"][0], problem_instance["parameter_indices"])
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            sums_sq_res_actual[0] / stdev **2, dof, 0.95)
        metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            sums_sq_res_actual[1] / stdev **2, dof, 0.95)

        # sensitivities and covariance matrix
        sens_snapshot = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance))
        sens_trajectories = common.utilities.sliceit_astrajectory(sens_snapshot)
        no_params = len(sens_problem_instance["parameters"])
        no_timepoints = len(sens_problem_instance["time"])
        cov_matrix = engine.estimation_matrices.compute_covariance_matrix(no_params, no_timepoints, sens_trajectories)

        # ellipsoid radius and confidence interval
        no_meas = common.utilities.size_it(problem_instance["outputs"])
        est_stdev = prototyping.statistical_inference.compute_measurements_standard_deviation( \
            sum_sq_res_actual, no_params, no_meas)
        ell_radius = prototyping.statistical_inference.compute_confidence_ellipsoid_radius( \
            no_params, no_meas, est_stdev, 0.9)
        confidence_intervals = prototyping.statistical_inference.compute_confidence_intervals( \
            cov_matrix, ell_radius)

        if do_reporting:
            print(problem_instance["parameters"])
            print(sum_sq_res_actual)
            print(sums_sq_res_actual)
            print(confidence_intervals)
            results.plot.plot_fit(problem_instance["time"], problem_instance["outputs"], predicted_values, act_meas_traj)
            results.plot.plot_residuals(problem_instance["time"], residuals_values)
            results.plot.plot_errors_and_residuals(problem_instance["time"], meas_noise_traj, residuals_values)
    

    def do_explore_solution_path(self, dv_path, model_instance, problem_instance, sens_model_instance, sens_problem_instance, stdev):
        do_reporting = False
        
        iterations = []
        objfunc_path = []
        objfunc_contribs_path = []
        ssr_path = []
        ssr_contribs_path = []
        conf_intervs_path = []
        dec_vars_path = []
        iter = 0
        for dvs in dv_path:
            iterations.append(iter)

            dec_vars = dvs[0]
            # objective function
            sum_sq_res = metrics.ordinary_differential.sum_squared_residuals_st( \
                dec_vars, models.ordinary_differential.linear_2p2s, model_instance, problem_instance)
            # objective-function contributions
            sums_sq_res = metrics.ordinary_differential.sums_squared_residuals( \
                dec_vars, models.ordinary_differential.linear_2p2s, model_instance, problem_instance)
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
            # sensitivities and covariance matrix
            sens_snapshot = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance))
            sens_trajectories = common.utilities.sliceit_astrajectory(sens_snapshot)
            no_params = len(sens_problem_instance["parameters"])
            no_timepoints = len(sens_problem_instance["time"])
            cov_matrix = engine.estimation_matrices.compute_covariance_matrix(no_params, no_timepoints, sens_trajectories)
            # ellipsoid radius and confidence interval
            no_meas = common.utilities.size_it(problem_instance["outputs"])
            est_stdev = prototyping.statistical_inference.compute_measurements_standard_deviation( \
                sum_sq_res, no_params, no_meas)
            ell_radius = prototyping.statistical_inference.compute_confidence_ellipsoid_radius( \
                no_params, no_meas, est_stdev, 0.9)
            confidence_intervals = prototyping.statistical_inference.compute_confidence_intervals( \
                cov_matrix, ell_radius)

            objfunc_path.append(sum_sq_res)
            objfunc_contribs_path.append(sums_sq_res)
            ssr_path.append(test_chisquared)
            ssr_contribs_path.append(tests_chisquared)
            conf_intervs_path.append(confidence_intervals)
            dec_vars_path.append(dec_vars)
            
            iter += 1

        global fig
        solvers.plot.set_plot_rows_and_cols(4, 4)
        solvers.plot.get_objective_function_plot(fig, iterations, objfunc_path)
        solvers.plot.get_objective_function_contributions_plot(fig, iterations, objfunc_contribs_path)
        solvers.plot.get_parameter_estimates_plot(fig, iterations, dec_vars_path)
        solvers.plot.get_confidence_intervals_plot(fig, iterations, conf_intervs_path)

        if do_reporting:
            solvers.plot.plot_objective_function(iterations, objfunc_path)
            solvers.plot.plot_objective_function_contributions(iterations, objfunc_contribs_path)
            solvers.plot.plot_chi_squared_test(iterations, ssr_path)
            solvers.plot.plot_chi_squared_tests(iterations, ssr_contribs_path)
            # TODO confidence intervals

        workflow_results = dict(results.report_workflows.workflow_data)
        workflow_results["params"] = copy.deepcopy(problem_instance["parameters"])
        workflow_results["obj"] = objfunc_path
        workflow_results["obj_contribs"] = objfunc_contribs_path
        workflow_results["ssr"] = ssr_path
        workflow_results["ssr_contribs"] = ssr_contribs_path
        workflow_results["conf_intervs"] = conf_intervs_path

        return workflow_results


    def test_workflow_st_linear_2p2s(self):
        # globals
        global fig
        fig = solvers.plot.get_figure()
        # TODO: user messages

        # configure
        do_reporting = False
        do_results = True
        dataset_id = '110110'
        ig_multiplier = 1.0
        # key-CG, key-Nelder-Mead 
        slv_method = solvers.solver_data.nonlinear_algebraic_methods["key-Nelder-Mead"]
        
        # setup
        all_results = dict(results.report_workflows.workflow_results)
        ref_model_instance, ref_problem_instance, model_instance, problem_instance, \
            sens_model_instance, sens_problem_instance, \
            stdev, act_meas_traj, exp_meas_traj, meas_noise_traj = self.do_setup()
        # TODO: why?
        tt = copy.deepcopy(problem_instance["time"])

        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        logger = solvers.least_squares.DecisionVariableLogger()
        algorithm_instance["callback"] = logger.log_decision_variables
        algorithm_instance["initial_guesses"] = copy.deepcopy(ref_problem_instance["parameters"]) * ig_multiplier
        algorithm_instance["method"] = slv_method
        
        # whole data set
        # least-squares
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            models.ordinary_differential.linear_2p2s, model_instance, problem_instance, algorithm_instance)
        problem_instance["parameters"] = result.x
        decision_variables = logger.get_decision_variables()

        self.do_workflow(model_instance, problem_instance, sens_model_instance, sens_problem_instance, \
            stdev, meas_noise_traj, act_meas_traj)
        all_results["full"] = self.do_explore_solution_path( \
            decision_variables, model_instance, problem_instance, sens_model_instance, sens_problem_instance, stdev)
        
        # slicing data
        if dataset_id == '101010':
            tm, emt, tmte, mne, tv, evt, tmtv, mnv = self.do_slice_data_101010(ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj)
        if dataset_id == '111000':
            tm, emt, tmte, mne, tv, evt, tmtv, mnv = self.do_slice_data_111000(ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj)
        if dataset_id == '000111':
            tm, emt, tmte, mne, tv, evt, tmtv, mnv = self.do_slice_data_000111(ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj)
        if dataset_id == '110110':
            tm, emt, tmte, mne, tv, evt, tmtv, mnv = self.do_slice_data_110110(ref_problem_instance, exp_meas_traj, meas_noise_traj, act_meas_traj)

        # calibration data set
        # least-squares
        problem_instance["outputs"] = emt
        problem_instance["time"] = tm

        logger = solvers.least_squares.DecisionVariableLogger()
        algorithm_instance["callback"] = logger.log_decision_variables
        algorithm_instance["initial_guesses"] = copy.deepcopy(ref_problem_instance["parameters"])
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            models.ordinary_differential.linear_2p2s, model_instance, problem_instance, algorithm_instance)
        problem_instance["parameters"] = result.x
        decision_variables = logger.get_decision_variables()
        
        self.do_workflow(model_instance, problem_instance, sens_model_instance, sens_problem_instance, stdev, mne, tmte)
        all_results["calibration"] = self.do_explore_solution_path( \
            decision_variables, model_instance, problem_instance, sens_model_instance, sens_problem_instance, stdev)

        # validation data set
        problem_instance["outputs"] = evt
        problem_instance["time"] = tv
        self.do_workflow(model_instance, problem_instance, sens_model_instance, sens_problem_instance, stdev, mnv, tmtv)
        all_results["validation"] = self.do_explore_solution_path( \
            decision_variables, model_instance, problem_instance, sens_model_instance, sens_problem_instance, stdev)
        
        # validation and calibration data set
        problem_instance["outputs"] = exp_meas_traj
        problem_instance["time"] = tt
        self.do_workflow(model_instance, problem_instance, sens_model_instance, sens_problem_instance, stdev, meas_noise_traj, act_meas_traj)
        all_results["calib+valid"] = self.do_explore_solution_path( \
            decision_variables, model_instance, problem_instance, sens_model_instance, sens_problem_instance, stdev)
        
        # results
        if do_results:
            fig.suptitle("Dataset-" + dataset_id)
            solvers.plot.show_figure()
        print(dataset_id)
        results.report_workflows.report_all(all_results)

        self.assertTrue(True)


    # this does a montecarlo randomisation of parameters
    # and computes the residuals
    def test_montecarlo_st_linear_2p2s(self):
        # configure
        do_reporting = False
        
        # setup
        rmi, rpi, mi, pi, smi, spi, \
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
            snapshots = solvers.initial_value.compute_trajectory_st( \
                models.ordinary_differential.linear_2p2s, mi, pi)
            trajectories = common.utilities.sliceit_astrajectory(snapshots)
            mc_outputs.append(trajectories)
            residuals = metrics.ordinary_differential.residuals_st( \
                models.ordinary_differential.linear_2p2s, mi, pi)
            mc_residuals.append(residuals)
            sums = metrics.ordinary_differential.sums_squared_residuals( \
                mct[ii], models.ordinary_differential.linear_2p2s, mi, pi)
            sums_mc_residuals.append(sums)

        pairs = numpy.transpose(sums_mc_residuals)
        if do_reporting:
            results.plot.plot_observation_ensembles(pi["time"], mc_outputs)
            results.plot.plot_observation_ensembles(pi["time"], mc_residuals)
            import matplotlib.pyplot as pp
            pp.plot(pairs[0], pairs[1], 'ro')
            pp.show()
        
        self.assertTrue(True)
        
                
    # this does a montecarlo randomisation of initial guesses
    # and solves the least-squares problem
    def test_montecarlo_multiple_optimisation_linear_2p2s(self):
        montecarlo_trials = 10
        dynamic_range = 1E3
        do_plotting = False
        slv_method = solvers.solver_data.nonlinear_algebraic_methods["key-CG"]

        ref_model_instance, ref_problem_instance, model_instance, problem_instance, \
            sens_model_instance, sens_problem_instance, \
            stdev, act_meas_traj, exp_meas_traj, meas_noise_traj = self.do_setup()

        ig = copy.deepcopy(ref_problem_instance["parameters"])
        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        algorithm_instance["initial_guesses"] = ig
        algorithm_instance["method"] = slv_method
        
        initial_guesses = []
        initial_guesses.append((data.generator.uniform_distribution(montecarlo_trials) -0.5)*2*dynamic_range)
        initial_guesses.append((data.generator.uniform_distribution(montecarlo_trials) -0.5)*2*dynamic_range)
        decision_variables = []
        for ii in range(montecarlo_trials):
            ig0 = []
            ig0.append(initial_guesses[0][ii])
            ig0.append(initial_guesses[1][ii]) 
            algorithm_instance["initial_guesses"] = ig0
            result = solvers.least_squares.solve_st( \
                metrics.ordinary_differential.sum_squared_residuals_st, \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, algorithm_instance)
            decision_variables.append(result.x)
        dvs = common.utilities.sliceit_astrajectory(decision_variables)
        mu = []
        mu.append(numpy.average(dvs[0]))
        mu.append(numpy.average(dvs[1]))
        sigma = []
        sigma.append(numpy.std(dvs[0]))
        sigma.append(numpy.std(dvs[1]))
        print("mu, sigma:", mu, sigma)
        if do_plotting:
            solvers.plot.plot_scatter(initial_guesses, [])
            solvers.plot.plot_scatter(dvs, [])


if __name__ == "__main__":
#    unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(RunLinearOdeExperiments("test_workflow_st_linear_2p2s"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
