
import copy
import numpy

import common.utilities
import metrics.ordinary_differential
import metrics.statistical_tests
import models.model_data_utils as mmdu
import engine.estimation_matrices
import engine.statistical_inference
import results.plot
import solvers.initial_value
import workflows.workflow_data


# TODO: do workflow fitting, do workflow no fitting
'''
compute SSR, total and contributions
compute residual trajectories, contributions
compute chi-squared test, total and contributions
compute confidence intervals
also compute: sensitivities, covariance matrix, estimate standard deviation
and ellipsoid radius
'''
def do_workflow_at_solution_point(model, model_instance, problem_instance, \
    sensitivity, sens_model_instance, sens_problem_instance, \
    stdev, meas_noise_traj, act_meas_traj):

    # config
    do_reporting = False
    
    # objective function
    sum_sq_res = metrics.ordinary_differential.sum_squared_residuals_st( \
        problem_instance["parameters"], model, model_instance, problem_instance)

    # objective-function contributions
    sums_sq_res = metrics.ordinary_differential.sums_squared_residuals( \
        problem_instance["parameters"], model, model_instance, problem_instance)

    # observables' trajectories
    predicted_snapshots = solvers.initial_value.compute_trajectory_st( \
        model, model_instance, problem_instance)
    predicted_values = common.utilities.sliceit_astrajectory(predicted_snapshots)
    
    # residuals' trajectories
    residuals_values = metrics.ordinary_differential.residuals_st( \
        model, model_instance, problem_instance)

    significance = problem_instance["confidence_region"]["confidence"]

    # global ssr test
    dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
        problem_instance["outputs"], problem_instance["parameter_indices"])
    ssr_test = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
        sum_sq_res / stdev **2, dof, significance)
    
    # observables' ssr test
    ssr_tests = []
    for ii in range(len(problem_instance["outputs"])):
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            problem_instance["outputs"][ii], problem_instance["parameter_indices"])
        ssr_tests.append( \
            metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
                sums_sq_res[ii] / stdev **2, dof, significance))

    # sensitivities and covariance matrix
    sens_snapshot = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
        sensitivity, sens_model_instance, sens_problem_instance))
    sens_trajectories = common.utilities.sliceit_astrajectory(sens_snapshot)

    no_obs = len(problem_instance["outputs"])
    no_params = len(sens_problem_instance["parameters"])
    no_timepoints = len(sens_problem_instance["time"])
    cov_matrix = engine.estimation_matrices.compute_covariance_matrix( \
        no_obs, no_params, no_timepoints, sens_trajectories)

    # ellipsoid radius and confidence interval
    no_meas = mmdu.calculate_number_of_observations(problem_instance["outputs"])
    est_var = engine.statistical_inference.compute_measurements_variance( \
        sum_sq_res, no_params, no_meas)
    ell_radius = engine.statistical_inference.compute_confidence_ellipsoid_radius( \
        no_params, no_meas, est_var, significance)
    confidence_intervals = engine.statistical_inference.compute_confidence_intervals( \
        cov_matrix, ell_radius)

    if do_reporting:
        print(problem_instance["parameters"])
        print(sum_sq_res)
        print(sums_sq_res)
        print(confidence_intervals)
        results.plot.plot_fit(problem_instance["time"], problem_instance["outputs"], predicted_values, act_meas_traj)
        results.plot.plot_residuals(problem_instance["time"], residuals_values)
        results.plot.plot_errors_and_residuals(problem_instance["time"], meas_noise_traj, residuals_values)
        
    workflow_results = dict(workflows.workflow_data.point_results)
    workflow_results["ssr"] = sum_sq_res
    workflow_results["ssrs"] = sums_sq_res
    workflow_results["ress_vals"] = residuals_values
    workflow_results["ssr_test"] = ssr_test
    workflow_results["ssrs_tests"] = ssr_tests  
    workflow_results["cov_matrix"] = cov_matrix
    workflow_results["est_var"] = est_var
    workflow_results["ell_radius"] = ell_radius
    workflow_results["conf_intvs"] = confidence_intervals

    return workflow_results


'''
compute SSR, total and contributions
compute residual trajectories, contributions
compute chi-squared test, total and contributions
compute confidence intervals
also compute: sensitivities, covariance matrix, estimate standard deviation
and ellipsoid radius
'''
def do_workflow_at_solution_path(model, model_instance, problem_instance, \
    sensitivity, sens_model_instance, sens_problem_instance, stdev, dv_path, fig):
    #config
    do_reporting = False
    
    iterations = []
    objfunc_path = []
    objfunc_contribs_path = []
    ssr_path = []
    ssr_contribs_path = []
    conf_intervs_path = []
    dec_vars_path = []
    iters = 0
    significance = problem_instance["confidence_region"]["confidence"]
    for dvs in dv_path:
        iterations.append(iters)

        dec_vars = dvs[0]
        # objective function
        sum_sq_res = metrics.ordinary_differential.sum_squared_residuals_st( \
            dec_vars, model, model_instance, problem_instance)
        # objective-function contributions
        sums_sq_res = metrics.ordinary_differential.sums_squared_residuals( \
            dec_vars, model, model_instance, problem_instance)
        # global ssr test
        dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
            problem_instance["outputs"], problem_instance["parameter_indices"])
        test_chisquared = metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            sum_sq_res / stdev **2, dof, significance)
        # observables' ssr test
        tests_chisquared = []
        for ii in range(len(problem_instance["outputs"])):
            dof = metrics.statistical_tests.calculate_degrees_of_freedom( \
                problem_instance["outputs"][ii], problem_instance["parameter_indices"])
            tests_chisquared.append(metrics.statistical_tests.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
                sums_sq_res[ii] / stdev **2, dof, significance))
        # sensitivities and covariance matrix
        sens_snapshot = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            sensitivity, sens_model_instance, sens_problem_instance))
        sens_trajectories = common.utilities.sliceit_astrajectory(sens_snapshot)
        no_obs = len(problem_instance["outputs"])
        no_params = len(sens_problem_instance["parameters"])
        no_timepoints = len(sens_problem_instance["time"])
        cov_matrix = engine.estimation_matrices.compute_covariance_matrix( \
            no_obs, no_params, no_timepoints, sens_trajectories)
        # ellipsoid radius and confidence interval
        no_meas = mmdu.calculate_number_of_observations(problem_instance["outputs"])
        est_var = engine.statistical_inference.compute_measurements_variance( \
            sum_sq_res, no_params, no_meas)
        ell_radius = engine.statistical_inference.compute_confidence_ellipsoid_radius( \
            no_params, no_meas, est_var, significance)
        confidence_intervals = engine.statistical_inference.compute_confidence_intervals( \
            cov_matrix, ell_radius)

        objfunc_path.append(sum_sq_res)
        objfunc_contribs_path.append(sums_sq_res)
        ssr_path.append(test_chisquared)
        ssr_contribs_path.append(tests_chisquared)
        conf_intervs_path.append(confidence_intervals)
        dec_vars_path.append(dec_vars)
        
        iters += 1

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

    workflow_results = dict(workflows.workflow_data.workflow_data)
    workflow_results["params"] = copy.deepcopy(problem_instance["parameters"])
    workflow_results["obj"] = objfunc_path
    workflow_results["obj_contribs"] = objfunc_contribs_path
    workflow_results["ssr"] = ssr_path
    workflow_results["ssr_contribs"] = ssr_contribs_path
    workflow_results["conf_intervs"] = conf_intervs_path
    algo_stats = dict(workflows.workflow_data.algorithmic_statistics)
    algo_stats["iters"] = iter
    workflow_results["algo_stats"] = algo_stats

    return workflow_results
