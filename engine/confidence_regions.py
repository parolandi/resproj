
import copy

import common.diagnostics as codi
import metrics.statistical_tests as mst
import models.model_data_utils as mmdu
import solvers.dynamic_optimisation as sdo
import solvers.monte_carlo_multiple_initial_value as mcmiv
# TODO: dependency, engine cannot depend on workflow
import workflows.protocols as wopr


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
    ssr = problem["nonlinear_confidence_region"]["ssr"]
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
    ssr = compute_chisquared_constraint( \
        best_point["objective_function"],
        problem["outputs"],
        problem["nonlinear_confidence_region"]["alpha"])
    problem["nonlinear_confidence_region"]["ssr"] = ssr

    hyperrectangle = compute_nonlinear_confidence_hyperrectangle(model, problem, algorithm)
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


# TODO: handle abnormal situations
def compute_nonlinear_confidence_interval(model, problem, algorithm, index):
    problem["nonlinear_confidence_region"]["parameter_index"] = index

    problem["performance_measure"] = sdo.maximise_it
    upper = sdo.solve(model, problem, algorithm)
    problem["performance_measure"] = sdo.minimise_it
    lower = sdo.solve(model, problem, algorithm)

    if (upper.status > 0 or lower.status > 0):
        codi.print_warning_error_code_message()

    return [lower.x[0], upper.x[0]]


def check_test(value, cutoff):
    if value < cutoff:
        return True
    return False


def compute_chisquared_constraint(ssr0, observations, confidence):
    n = mmdu.calculate_number_of_observations(observations)
    chisquaredvalue = mst.calculate_one_sided_chi_squared_value(confidence, 1)
    ssr = ssr0 + chisquaredvalue/n
    return ssr

# -----------------------------------------------------------------------------

def compute_linearised_confidence_region_ellipsoid(config, best_point):
    """
    return numpy.matrix
    """
    workflow_results = wopr.do_sensitivity_based_workflow_at_solution_point(config, best_point)
    cov_matrix = workflow_results["cov_matrix"]
    ell_radius = workflow_results["ell_radius"]
    std_cov_matrix = cov_matrix * ell_radius
    return std_cov_matrix


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
