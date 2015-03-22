
import copy
import numpy

import common.diagnostics as codi
import engine.statistical_inference as enstin
import metrics.statistical_tests as mst
import models.model_data_utils as mmdu
import solvers.dynamic_optimisation as sdo
import solvers.monte_carlo_multiple_initial_value as mcmiv
# TODO: dependency, engine cannot depend on workflow
import workflows.protocols as wopr


"""
Best point is used as initial guess to start single-parameter search in order to
find interval limits from which region can be approximated; it is also used
to establish the threshold constraint based on the optimum SSR
"""
def compute_nonlinear_confidence_region_points(model, problem, algorithm_rf, algorithm_mc, best_point):
    """
    returns solvers.monte_carlo_multiple_initial_value.ensemble_trajectoryies
    """
    hyperrect = compute_nonlinear_confidence_intervals(model, problem, algorithm_rf, best_point)
    hyper = []
    for ii in range(len(hyperrect)):
        hyper.append(tuple(hyperrect[ii]))
    algorithm_mc["decision_variable_ranges"] = hyper
    hyperpnts = evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals(model, problem, algorithm_mc)
    ssr = problem["confidence_region"]["ssr"]
    pnts = filter_nonlinear_confidence_region_points(hyperpnts, ssr)
    return pnts


def compute_nonlinear_confidence_region_points_extremal(model, problem, algorithm_rf, algorithm_mc, best_point):
    """
    returns solvers.monte_carlo_multiple_initial_value.ensemble_trajectoryies
    """
    hyperrect = compute_nonlinear_confidence_intervals_extremal(model, problem, algorithm_rf, best_point)
    hyper = []
    for ii in range(len(hyperrect)):
        hyper.append(tuple(hyperrect[ii]))
    algorithm_mc["decision_variable_ranges"] = hyper
    hyperpnts = evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals(model, problem, algorithm_mc)
    ssr = problem["confidence_region"]["ssr"]
    pnts = filter_nonlinear_confidence_region_points(hyperpnts, ssr)
    return pnts


def filter_nonlinear_confidence_region_points(hyper, cutoff):
    hypo = copy.deepcopy(mcmiv.ensemble_trajectoryies)
    for ii in range(len(hyper["objective_function"])):
        if (check_test(hyper["objective_function"][ii], cutoff)):
            hypo["objective_function"].append(hyper["objective_function"][ii])
            hypo["decision_variables"].append(hyper["decision_variables"][ii])
    return hypo


def evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals(model, problem, algorithm):
    result = mcmiv.solve(model, problem, algorithm)
    points = result["succeeded"]["decision_variables"]
    ssrs = result["succeeded"]["objective_function"]
    hyper = copy.deepcopy(mcmiv.ensemble_trajectoryies)
    hyper["objective_function"] = ssrs
    hyper["decision_variables"] = points
    return hyper


def compute_nonlinear_confidence_intervals(model, problem, algorithm, best_point):
    mmdu.apply_decision_variables_to_parameters(best_point, model, problem)
    ssr = compute_f_constraint( \
        best_point["objective_function"],
        problem["outputs"],
        len(problem["parameter_indices"]),
        problem["confidence_region"]["confidence"])
    problem["confidence_region"]["ssr"] = ssr

    hyperrectangle = compute_nonlinear_confidence_hyperrectangle(model, problem, algorithm)
    return hyperrectangle


def compute_nonlinear_confidence_intervals_extremal(model, problem, algorithm, best_point):
    mmdu.apply_decision_variables_to_parameters(best_point, model, problem)
    ssr = compute_f_constraint( \
        best_point["objective_function"],
        problem["outputs"],
        len(problem["parameter_indices"]),
        problem["confidence_region"]["confidence"])
    problem["confidence_region"]["ssr"] = ssr

    hyperrectangle = compute_nonlinear_confidence_hyperrectangle_extremal(model, problem, algorithm)
    return hyperrectangle


def compute_nonlinear_confidence_hyperrectangle(model, problem, algorithm):
    hyperrectangle = []
    func = problem["performance_measure"]
    opt_param = copy.deepcopy(problem["parameters"])
    for param_index in range(len(problem["parameter_indices"])):
        interval = compute_nonlinear_confidence_interval(model, problem, algorithm, param_index)
        hyperrectangle.append(interval)
        problem["parameters"] = copy.deepcopy(opt_param)
        model["parameters"] = copy.deepcopy(opt_param)
    problem["performance_measure"] = func
    return hyperrectangle


def compute_nonlinear_confidence_hyperrectangle_extremal(model, problem, algorithm):
    hyperrectangle = []
    func = problem["performance_measure"]
    opt_param = copy.deepcopy(problem["parameters"])
    for param_index in range(len(problem["parameter_indices"])):
        interval = compute_nonlinear_confidence_interval_extremal(model, problem, algorithm, param_index)
        hyperrectangle.append(interval)
        problem["parameters"] = copy.deepcopy(opt_param)
        model["parameters"] = copy.deepcopy(opt_param)
    problem["performance_measure"] = func
    return hyperrectangle


# TODO: handle abnormal situations
def compute_nonlinear_confidence_interval(model, problem, algorithm, index):
    problem["confidence_region"]["parameter_index"] = index

    problem["performance_measure"] = sdo.maximise_it
    upper = sdo.solve(model, problem, algorithm)
    problem["performance_measure"] = sdo.minimise_it
    lower = sdo.solve(model, problem, algorithm)

    if (upper.status > 0 or lower.status > 0):
        codi.print_warning_error_code_message()

    return [lower.x[0], upper.x[0]]


def maximise_distance_upper(x, x0, index):
    delta = (-1) * (x[index] - x0[index])
    return delta


def maximise_distance_lower(x, x0, index):
    delta = (x[index] - x0[index])
    return delta


def compute_nonlinear_confidence_interval_extremal(model, problem, algorithm, index):
    problem["confidence_region"]["parameter_index"] = index

    # form objective function
    problem["performance_measure"] = maximise_distance_upper
    p0 = copy.deepcopy(problem["parameters"])
    problem["performance_measure_args"] = tuple([p0, index])

    # forming constraints here as this is the right level of abstraction
    # copy existing constraints back
    problem["constraints"] = form_constraints(model, problem)

    # form bounds
    algorithm["initial_guesses"] = numpy.asarray(problem["parameters"]) * 1.01
    bounds = []
    for _ in range(len(problem["parameters"])):
        bounds.append([-10, 10])
    bounds[index][0] = problem["parameters"][index]
    problem["bounds"] = tuple(bounds)

    upper = sdo.solve_std(model, problem, algorithm)

    if (upper.status > 0):
        codi.print_warning_error_code_message()

    # form objective function
    problem["performance_measure"] = maximise_distance_lower
    # maintain arguments
    
    # forming constraints here as this is the right level of abstraction
    # copy existing constraints back
    problem["constraints"] = form_constraints(model, problem)
    
    # form bounds
    algorithm["initial_guesses"] = numpy.asarray(problem["parameters"]) * 0.99
    bounds = []
    for _ in range(len(problem["parameters"])):
        bounds.append([-10, 10])
    bounds[index][1] = problem["parameters"][index]
    problem["bounds"] = tuple(bounds)
    
    lower = sdo.solve_std(model, problem, algorithm)

    if (upper.status > 0 or lower.status > 0):
        codi.print_warning_error_code_message()

    return [lower.x[index], upper.x[index]]


# unit-tested
def likelihood_constraint(x, model_data, problem_data, ssr_0):
    assert(len(x) == len(model_data["parameters"]))
    assert(len(x) == len(problem_data["parameters"]))
    assert(problem_data["confidence_region"]["performance_measure"] is not None)

    model_data["parameters"] = x
    problem_data["parameters"] = x
    ssr = problem_data["confidence_region"]["performance_measure"](None, None, model_data, problem_data)
    return ssr_0 - ssr


def positive_delta_constraint(x, x0, index):
    return x[index] - x0[index]


def negative_delta_constraint(x, x0, index):
    return x0[index] - x[index]


def form_constraints(model, problem):
    ssr0 = problem["confidence_region"]["ssr"]
    constraint_list = []
    constraint_list.append( \
                  {'type': 'ineq', \
                   'fun': likelihood_constraint, \
                   'args': (model, problem, ssr0)})
    constraints = tuple(constraint_list)
    return constraints


# unit-tested
def form_upper_constraints(model, problem):
    x0 = copy.deepcopy(problem["parameters"])
    ssr0 = problem["confidence_region"]["ssr"]
    constraint_list = []
    constraint_list.append( \
                  {'type': 'ineq', \
                   'fun': likelihood_constraint, \
                   'args': (model, problem, ssr0)})
    for ii in range(len(problem["parameters"])):
        constraint_list.append( \
                       {'type': 'ineq', \
                        'fun': positive_delta_constraint, \
                        'args': (x0, ii)})
    constraints = tuple(constraint_list)
    return constraints


def form_lower_constraints(model, problem):
    x0 = copy.deepcopy(problem["parameters"])
    ssr0 = problem["confidence_region"]["ssr"]
    constraint_list = []
    constraint_list.append( \
                  {'type': 'ineq', \
                   'fun': likelihood_constraint, \
                   'args': (model, problem, ssr0)})
    for ii in range(len(problem["parameters"])):
        constraint_list.append( \
                       {'type': 'ineq', \
                        'fun': negative_delta_constraint, \
                        'args': (x0, ii)})
    constraints = tuple(constraint_list)
    return constraints


def check_test(value, cutoff):
    if value < cutoff:
        return True
    return False


# TODO: not tested
def compute_chisquared_constraint(ssr0, observations, confidence):
    assert(False)

    n = mmdu.calculate_number_of_observations(observations)
    chisquaredvalue = mst.calculate_one_sided_chi_squared_value(confidence, 1)
    ssr = ssr0 + chisquaredvalue/n
    return ssr


def compute_f_constraint(ssr0, observations, no_params, confidence):
    no_meas = mmdu.calculate_number_of_observations(observations)
    f_value = enstin.compute_one_sided_f_value(confidence, no_meas, no_params)
    est_var = enstin.compute_measurements_variance(ssr0, no_params, no_meas)
    ssr = ssr0 + est_var * no_params * f_value
    return ssr


# -----------------------------------------------------------------------------

"""
Best point is to compute local parametric sensitivities and to calculate
the estimated variance based on the optimum SSR
"""
def compute_linearised_confidence_region_ellipsoid(config, best_point):
    """
    return numpy.matrix
    """
    workflow_results = wopr.do_sensitivity_based_workflow_at_solution_point(config, best_point)
    cov_matrix = workflow_results["cov_matrix"]
    ell_radius = workflow_results["ell_radius"]
    std_cov_matrix = cov_matrix * ell_radius
    return std_cov_matrix


"""
Best point is to compute local parameteric sensitivities and to calculate
the estimated variance based on the optimum SSR
"""
def compute_linearised_confidence_intervals(config, best_point):
    """
    return list of list (list of intervals)
    """
    workflow_results = wopr.do_sensitivity_based_workflow_at_solution_point(config, best_point)
    intervals = workflow_results["conf_intvs"]
    nominal = best_point["decision_variables"]
    hyperrectangle = []
    for ii in range(len(intervals)):
        hyperrectangle.append([nominal[ii]-intervals[ii], nominal[ii]+intervals[ii]])
    return hyperrectangle
