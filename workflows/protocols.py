
import copy
import numpy

import metrics.ordinary_differential as mod
import metrics.statistical_tests as mst
import models.model_data as mmd
import models.model_data_utils as mmdu
import engine.statistical_inference as esi
import engine.estimation_matrices as eem
import setups.setup_data_utils as ssdu
import solvers.initial_value as siv
import solvers.least_squares as sls
import solvers.local_sensitivities as sse
import workflows.workflow_data as wwd


'''
Do calibration
Compute performance measure
config: setups.setup_data.experiment_setup
return: models.model_data.optimisation_problem_point
    the decision variable values
    the objective function value
'''
def do_calibration_and_compute_performance_measure(config):
    # setup
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["calib"])
    algorithm_instance = config["algorithm_setup"](None)

    # least-squares
    result = sls.solve(model_instance, problem_instance, algorithm_instance)

    # verification    
    # WIP: should this be needed?
    # need to do this here because problem data is kind of ignored
    problem_instance["parameters"] = copy.deepcopy(result.x)
    for ii in range(len(problem_instance["parameter_indices"])):
        model_instance["parameters"][problem_instance["parameter_indices"][ii]] = copy.deepcopy(result.x[ii])

    ssr_fit = problem_instance["performance_measure"](None, None, model_instance, problem_instance)

    calib_sol = dict(mmd.optimisation_problem_point)
    calib_sol["decision_variables"] = numpy.asarray(copy.deepcopy(problem_instance["parameters"]))
    calib_sol["objective_function"] = ssr_fit
    return calib_sol 


def do_validation_and_compute_performance_measure_at_solution_point(config, solution_point):
    # setup
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["valid"])

    # verification    
    # WIP: should this be needed?
    # need to do this here because problem data is kind of ignored
    problem_instance["parameters"] = copy.deepcopy(solution_point["decision_variables"])
    for ii in range(len(problem_instance["parameter_indices"])):
        model_instance["parameters"][problem_instance["parameter_indices"][ii]] = copy.deepcopy(solution_point["decision_variables"][ii])

    ssr_fit = problem_instance["performance_measure"](None, None, model_instance, problem_instance)

    valid_sol = copy.deepcopy(solution_point)
    valid_sol["objective_function"] = ssr_fit
    return valid_sol 


'''
Compute SSR, total and contributions
Compute residual trajectories, contributions
Compute chi-squared test, total and contributions
config: setups.setup_data.experiment_setup
solution_point: models.model_data.optimisation_problem_point
return: workflows.workflow_data.system_based_point_results
'''
# TODO: hard-coded stdev
# TODO: change basic to system_based
# TODO: change to at any point
def do_basic_workflow_at_solution_point(config, solution_point):
    assert(solution_point is not None)
    # TODO: preconditions!
    
    # TODO: hard-coded stdev
    stdev = 1.0

    # setup
    protocol = config["protocol_setup"]()
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    protocol_step = ssdu.get_next_protocol_step(config)
    problem_instance = config["problem_setup"](model_instance, data_instance[protocol_step])
    
    mmdu.apply_decision_variables_to_parameters(solution_point, model_instance, problem_instance)
    
    assert(problem_instance["performance_measure"] is protocol["performance_measure"])
    assert(problem_instance["performance_measure"] is mod.sum_squared_residuals_st)

    # objective function
    sum_sq_res = mod.sum_squared_residuals_st(None, None, model_instance, problem_instance)

    # objective-function contributions
    sums_sq_res = mod.sums_squared_residuals(None, None, model_instance, problem_instance)

    # observables' trajectories
    if False:
        _ = siv.compute_timecourse_trajectories(None, model_instance, problem_instance)
     
    # residuals' trajectories
    residuals_values = mod.residuals_st(None, model_instance, problem_instance)

    # global ssr test
    dof = mst.calculate_degrees_of_freedom( \
        problem_instance["outputs"], problem_instance["parameter_indices"])
    ssr_test = mst.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
        sum_sq_res / stdev **2, dof, 0.95)
    ssr_thresh_lb, ssr_thresh_ub = \
        mst.calculate_thresholds_two_sided_chi_squared_test_for_mean_sum_squared_residuals(dof, 0.95)
    
    # observables' ssr test
    ssr_tests = []
    ssrs_thresh_lb = []
    ssrs_thresh_ub = []
    for ii in range(len(problem_instance["outputs"])):
        dof = mst.calculate_degrees_of_freedom( \
            problem_instance["outputs"][ii], problem_instance["parameter_indices"])
        ssr_tests.append( \
            mst.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
                sums_sq_res[ii] / stdev **2, dof, 0.95))
        thresh_lb, thresh_up = \
            mst.calculate_thresholds_two_sided_chi_squared_test_for_mean_sum_squared_residuals(dof, 0.95)
        ssrs_thresh_lb.append(thresh_lb)
        ssrs_thresh_ub.append(thresh_up)

    workflow_results = dict(wwd.system_based_point_results)
    workflow_results["params"] = copy.deepcopy(problem_instance["parameters"])
    workflow_results["ssr"] = sum_sq_res
    workflow_results["ssrs"] = sums_sq_res
    workflow_results["ress_vals"] = residuals_values
    workflow_results["ssr_test"] = ssr_test
    workflow_results["ssrs_tests"] = ssr_tests  

    workflow_results["ssr_thresh_lb"] = ssr_thresh_lb
    workflow_results["ssr_thresh_ub"] = ssr_thresh_ub
    workflow_results["ssrs_thresh_lb"] = ssrs_thresh_lb
    workflow_results["ssrs_thresh_ub"] = ssrs_thresh_ub


    return workflow_results


'''
Compute sensitivities, covariance matrix,
estimated standard deviation, ellipsoid radius and confidence intervals
config: setups.setup_data.experiment_setup
solution_point:
return: workflows.workflow_data.sensitivity_based_point_results
'''
# TODO: change to at any point
def do_sensitivity_based_workflow_at_solution_point(config, solution_point):
    assert(solution_point is not None)
    # TODO: preconditions!
    ssr = solution_point["objective_function"]

    # full sensitivities
    state_and_sens_trajectories = []
    data_instance = config["data_setup"]()
    protocol_step = ssdu.get_next_protocol_step(config)
    if config["sensitivity_setup"] is sse.compute_timecourse_trajectories_and_sensitivities:
        model_instance = config["model_setup"]()
        problem_instance  = config["problem_setup"](model_instance, data_instance[protocol_step])
        mmdu.apply_decision_variables_to_parameters(solution_point, model_instance, problem_instance)
        state_and_sens_trajectories = config["sensitivity_setup"](model_instance, problem_instance)
    else:
        # TODO: use config; if possible refactor
        assert(config["sensitivity_model_setup"] is not None)
        model_instance = config["sensitivity_model_setup"]()
        problem_instance  = config["sensitivity_problem_setup"](model_instance, data_instance[protocol_step])
        mmdu.apply_decision_variables_to_parameters(solution_point, model_instance, problem_instance)
        state_and_sens_trajectories = siv.compute_timecourse_trajectories( \
            None, model_instance, problem_instance)
    
    system_model = config["model_setup"]()
    dim_states = len(system_model["states"])
    sens_trajectories = mmdu.get_sensitivity_trajectories( \
        dim_states, problem_instance, state_and_sens_trajectories)

    # covariance matrix
    no_obs = len(problem_instance["outputs"])
    no_params = mmdu.get_number_of_decision_variables(problem_instance)
    no_timepoints = mmdu.get_number_of_time_points(problem_instance)
    cov_matrix = eem.compute_covariance_matrix(no_obs, no_params, no_timepoints, sens_trajectories)
    corr_matrix = eem.calculate_correlation_matrix(cov_matrix)

    # ellipsoid radius and confidence interval
    no_meas = mmdu.calculate_number_of_observations(problem_instance["outputs"])
    est_stdev = esi.compute_measurements_standard_deviation(ssr, no_params, no_meas)
    ell_radius = esi.compute_confidence_ellipsoid_radius(no_params, no_meas, est_stdev, 0.9)
    confidence_intervals = esi.compute_confidence_intervals(cov_matrix, ell_radius)

    workflow_results = dict(wwd.sensitivity_based_point_results)
    workflow_results["params"] = copy.deepcopy(problem_instance["parameters"])
    workflow_results["cov_matrix"] = cov_matrix
    workflow_results["cov_det"] = eem.calculate_determinant(cov_matrix)
    workflow_results["est_stdev"] = est_stdev
    workflow_results["ell_radius"] = ell_radius
    workflow_results["conf_intvs"] = confidence_intervals
    workflow_results["corr_matrix"] = corr_matrix
    workflow_results["corr_det"] = eem.calculate_determinant(corr_matrix)

    return workflow_results
