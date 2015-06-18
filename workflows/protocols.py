
import copy
import logging
import numpy

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

import hack.hacks


thresholded_value = {
    "value": 0.0,
    "lb": 0.0,
    "ub": 0.0,
    }


linearised_parametric_uncertainty = {
    "cov_matrix": None,
    "cov_det": 0.0,
    "est_var": 0.0,
    "ell_radius": 0.0,
    "conf_intvs": [],
    "corr_matrix": None,
    "corr_det": 0.0,
    }


def do_calibration_and_compute_performance_measure(config):
    """
    Do calibration
    Compute performance measure
    config: setups.setup_data.experiment_setup
    return: models.model_data.optimisation_problem_point
    """
    # setup
    # TODO: 2015-05-15, reuse
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["calib"])
    algorithm_instance = config["algorithm_setup"](None)

    # least-squares
    result = sls.solve(model_instance, problem_instance, algorithm_instance)

    # verification    
    # WIP: 2015-05-15, should this be needed?
    # need to do this here because problem data is kind of ignored
    problem_instance["parameters"] = copy.deepcopy(result.x)
    for ii in range(len(problem_instance["parameter_indices"])):
        model_instance["parameters"][problem_instance["parameter_indices"][ii]] = copy.deepcopy(result.x[ii])

    ssr_fit = problem_instance["performance_measure"](None, model_instance, problem_instance)

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
    # WIP: 2015-05-15, should this be needed?
    # need to do this here because problem data is kind of ignored
    problem_instance["parameters"] = copy.deepcopy(solution_point["decision_variables"])
    for ii in range(len(problem_instance["parameter_indices"])):
        model_instance["parameters"][problem_instance["parameter_indices"][ii]] = \
            copy.deepcopy(solution_point["decision_variables"][ii])

    ssr_fit = problem_instance["performance_measure"](None, model_instance, problem_instance)

    valid_sol = copy.deepcopy(solution_point)
    valid_sol["objective_function"] = ssr_fit
    return valid_sol 


def do_global_ssr_test(problem_instance, sum_sq_res, stdev):
    '''
    return    thresholded_value
    '''
    ssr_test = dict(thresholded_value)
    significance = problem_instance["confidence_region"]["confidence"]
    dof = mst.calculate_degrees_of_freedom( \
        problem_instance["outputs"], problem_instance["parameter_indices"])
    ssr_test["value"] = mst.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
        sum_sq_res / stdev **2, dof, significance)
    ssr_test["lb"], ssr_test["ub"] = \
        mst.calculate_thresholds_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            dof, significance)
    return ssr_test


def do_observables_ssr_tests(problem_instance, sums_sq_res, stdev):
    '''
    return    list of thresholded_value's
    '''
    significance = problem_instance["confidence_region"]["confidence"]
    ssr_tests = []
    for ii in range(len(problem_instance["outputs"])):
        ssr_test = dict(thresholded_value)
        dof = mst.calculate_degrees_of_freedom( \
            problem_instance["outputs"][ii], problem_instance["parameter_indices"])
        ssr_test["value"] = mst.calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
            sums_sq_res[ii] / stdev **2, dof, significance)
        ssr_test["lb"], ssr_test["ub"] = \
            mst.calculate_thresholds_two_sided_chi_squared_test_for_mean_sum_squared_residuals( \
                dof, significance)
        ssr_tests.append(ssr_test)
    return ssr_tests


def convert_to_system_based_workflow_results(problem_instance, sum_sq_res, sums_sq_res, ssr_test, ssr_tests):
    workflow_results = dict(wwd.system_based_point_results)
    workflow_results["params"] = copy.deepcopy(problem_instance["parameters"])
    workflow_results["ssr"] = sum_sq_res
    workflow_results["ssrs"] = sums_sq_res
    workflow_results["ssr_test"] = ssr_test["value"]
    workflow_results["ssr_thresh_lb"] = ssr_test["lb"]
    workflow_results["ssr_thresh_ub"] = ssr_test["ub"]
    for ii in range(len(problem_instance["outputs"])):
        workflow_results["ssrs_tests"].append(ssr_tests[ii]["value"])  
        workflow_results["ssrs_thresh_lb"].append(ssr_tests[ii]["lb"])
        workflow_results["ssrs_thresh_ub"].append(ssr_tests[ii]["ub"])
    return workflow_results


# TODO: hard-coded stdev
# TODO: change basic to system_based
# TODO: change to at any point
# TODO: 2015-05-28; solution_point can be None
def do_basic_workflow_at_solution_point(config, solution_point):
    '''
    Compute SSR; total and contributions
    Compute chi-squared test; total and contributions
    config:         setups.setup_data.experiment_setup
    solution_point: models.model_data.optimisation_problem_point
    return:         workflows.workflow_data.system_based_point_results
    '''
    assert(solution_point is not None)
    # TODO: preconditions!

    stdev = hack.hacks.get_stdev()
    # setup
    model_instance, problem_instance, protocol = \
        ssdu.get_model_problem_protocol(config)
    mmdu.apply_decision_variables_to_parameters(solution_point, model_instance, problem_instance)
    assert(problem_instance["performance_measure"] is protocol["performance_measure"])
    # objective function
    sum_sq_res = problem_instance["performance_measure"](None, model_instance, problem_instance)
    # objective-function contributions
    sums_sq_res = problem_instance["performance_observables"](model_instance, problem_instance)
    # statistical tests
    ssr_test = do_global_ssr_test(problem_instance, sum_sq_res, stdev)
    ssr_tests = do_observables_ssr_tests(problem_instance, sums_sq_res, stdev)
    # return value
    workflow_results = convert_to_system_based_workflow_results( \
        problem_instance, sum_sq_res, sums_sq_res, ssr_test, ssr_tests)
    logging.info("workflows.protocols.do_basic_workflow_at_solution_point")
    logging.info(workflow_results)
    return workflow_results


def do_linearised_parametric_uncertainty(problem_instance, ssr, sens_trajectories):
    significance = problem_instance["confidence_region"]["confidence"]
    no_obs = len(problem_instance["outputs"])
    no_meas = mmdu.calculate_number_of_observations(problem_instance["outputs"])
    no_params = mmdu.get_number_of_decision_variables(problem_instance)
    no_timepoints = mmdu.get_number_of_time_points(problem_instance)

    lin_par_unc = dict(linearised_parametric_uncertainty)
    lin_par_unc["cov_matrix"] = eem.compute_covariance_matrix(no_obs, no_params, no_timepoints, sens_trajectories)
    cov_matrix = lin_par_unc["cov_matrix"]
    lin_par_unc["corr_matrix"] = eem.calculate_correlation_matrix(cov_matrix)
    corr_matrix = lin_par_unc["corr_matrix"]
    lin_par_unc["est_var"] = esi.compute_measurements_variance(ssr, no_params, no_meas)
    est_var = lin_par_unc["est_var"]
    lin_par_unc["ell_radius"] = esi.compute_confidence_ellipsoid_radius(no_params, no_meas, est_var, significance)
    lin_par_unc["conf_intvs"] = esi.compute_confidence_intervals( \
        cov_matrix, mst.calculate_two_sided_t_student_value(significance, no_meas, no_params))
    lin_par_unc["cov_det"] = eem.calculate_determinant(cov_matrix)
    lin_par_unc["corr_det"] = eem.calculate_determinant(corr_matrix)
    return lin_par_unc

def convert_to_sensitivity_based_workflow_results(problem_instance, lin_par_unc):
    workflow_results = dict(wwd.sensitivity_based_point_results)
    workflow_results["params"] = copy.deepcopy(problem_instance["parameters"])
    workflow_results["cov_matrix"] = lin_par_unc["cov_matrix"]
    workflow_results["cov_det"] = lin_par_unc["cov_det"]
    workflow_results["est_var"] = lin_par_unc["est_var"]
    workflow_results["ell_radius"] = lin_par_unc["ell_radius"]
    workflow_results["conf_intvs"] = lin_par_unc["conf_intvs"]
    workflow_results["corr_matrix"] = lin_par_unc["corr_matrix"]
    workflow_results["corr_det"] = lin_par_unc["corr_det"]
    return workflow_results


def get_conditional_model_and_problem(config, solution_point):
    data_instance = config["data_setup"]()
    protocol_step = ssdu.get_next_protocol_step(config)
    if config["sensitivity_setup"] is sse.compute_timecourse_trajectories_and_sensitivities:
        model_instance = config["model_setup"]()
        problem_instance  = config["problem_setup"](model_instance, data_instance[protocol_step])
    else:
        # TODO: use config; if possible refactor
        assert(config["sensitivity_model_setup"] is not None)
        model_instance = config["sensitivity_model_setup"]()
        problem_instance  = config["sensitivity_problem_setup"](model_instance, data_instance[protocol_step])
    mmdu.apply_decision_variables_to_parameters(solution_point, model_instance, problem_instance)
    return model_instance, problem_instance


# TODO: 2015-05-28; extract to engine
def compute_sensitivity_trajectories(config, model_instance, problem_instance):
    # full sensitivities
    state_and_sens_trajectories = []
    if config["sensitivity_setup"] is sse.compute_timecourse_trajectories_and_sensitivities:
        state_and_sens_trajectories = config["sensitivity_setup"](model_instance, problem_instance)
    else:
        state_and_sens_trajectories = siv.compute_timecourse_trajectories( \
            None, model_instance, problem_instance)
    
    system_model = config["model_setup"]()
    dim_states = len(system_model["states"])
    sens_trajectories = mmdu.get_sensitivity_trajectories( \
        dim_states, problem_instance, state_and_sens_trajectories)
    return sens_trajectories


# TODO: change to at any point
# TODO: 2015-05-28; solution_point can be None
def do_sensitivity_based_workflow_at_solution_point(config, solution_point):
    """
    Compute sensitivities, covariance matrix,
    estimated standard deviation, ellipsoid radius and confidence intervals
    config: setups.setup_data.experiment_setup
    solution_point:
    return: workflows.workflow_data.sensitivity_based_point_results
    """
    assert(solution_point is not None)
    # TODO: preconditions!
    ssr = solution_point["objective_function"]

    # TODO: config for problem_instance?
    model_instance, problem_instance = get_conditional_model_and_problem(config, solution_point)
    sens_trajectories = compute_sensitivity_trajectories(config, model_instance, problem_instance)
    lin_par_unc = do_linearised_parametric_uncertainty(problem_instance, ssr, sens_trajectories)
    workflow_results = convert_to_sensitivity_based_workflow_results(problem_instance, lin_par_unc)
    logging.info("workflows.protocols.do_sensitivity_based_workflow_at_solution_point")
    logging.info(workflow_results)
    return workflow_results
