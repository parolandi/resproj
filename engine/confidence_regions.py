
import copy
import logging
import math
import numpy
import time

import common.diagnostics as codi
import engine.diagnostics as endi
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
    logging.info(hyperrect)
    hyper = []
    for ii in range(len(hyperrect)):
        hyper.append(tuple(hyperrect[ii]))
    algorithm_mc["decision_variable_ranges"] = hyper
    hyperpnts = evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals(model, problem, algorithm_mc)
    ssr = problem["confidence_region"]["ssr"]
    pnts = filter_nonlinear_confidence_region_points(hyperpnts, ssr)
    return pnts


# TODO: 2015-07-09; parameterise constants
def trim_hyperrectangle_ranges(problem, hyperrect):
    if len(problem["decision_variables"]) == 0:
        logging.warn("NCR hyperrect: no decision variables found!")
        return hyperrect
    
    optimal_estimates = copy.deepcopy(problem["decision_variables"])
    logging.info("NCR hyperrect uncorrected: " + str(hyperrect))
    for ii in range(len(optimal_estimates)):
        if hyperrect[ii][0] < optimal_estimates[ii] * 0.1 or math.isnan(hyperrect[ii][0]):
            hyperrect[ii][0] = optimal_estimates[ii] * 0.1
        if hyperrect[ii][1] > optimal_estimates[ii] * 10 or math.isnan(hyperrect[ii][1]):
            hyperrect[ii][1] = optimal_estimates[ii] * 10
    
    logging.info("NCR hyperrect corrected: " + str(hyperrect))
    return hyperrect


def compute_nonlinear_confidence_region_extremal_internal(model, problem, algorithm_rf, algorithm_mc, best_point):
    """
    internal
    """
    logging.debug("engine.confidence_regions.compute_nonlinear_confidence_region_extremal_internal")
    # HACK
    hyperrect, statuses = compute_nonlinear_confidence_intervals_extremal(model, problem, algorithm_rf, best_point)
    
    # HACK 2015-09-14
    lc = 0.75
    uc = 1.25
    '''
    # yesnoyes
    hyperrect = [ \
        [5.303839254978861e-05*lc, 6.7928643137517991e-05*uc], \
        [5900150.185800408*lc, 0.1*59065454.091839552*uc], \
        [0.01009237303638489*lc, 0.01429891307608047*uc], \
        [0.018628141421802392*lc, 0.033995558368361149*uc]]
    # yesyesno
    hyperrect = [ \
        [0.000067, 0.000076], \
        [5000000, 7100000], \
        [0.0052, 0.022], \
        [0.0063/3, 1.85e-01*3]]
    hyperrect = [ \
        [0.000068, 0.000076], \
        [5300000, 6800000], \
        [0.0062, 0.022], \
        [0.0063, 0.082]]
    '''
    """
    hyperrect = [ \
        [7.1815198110426653e-05*lc, 7.2828378864918741e-05*uc], \
        [5927979.0165858017*lc, 5928271.2840146916*uc], \
        [0.012124961140420856, 0.012124961140420856], \
        [0.017173506980212713, 0.017173506980212713]]
    hyperrect = [ \
        [0.000069, 0.000075], \
        [5553991, 6327361], \
        [0.012124961140420856/2, 0.012124961140420856*2], \
        [0.017173506980212713/2, 0.017173506980212713*2]]
    hyperrect = [ \
        [0.000059, 0.000085], \
        [5053991, 6827361], \
        [0.012124961140420856/5, 0.012124961140420856*5], \
        [0.017173506980212713/5, 0.017173506980212713*5]]
    hyperrect = [ \
        [0.000069, 0.000075], \
        [5400000, 6400000], \
        [0.012124961140420856/5, 0.012124961140420856*5], \
        [0.017173506980212713/5, 0.017173506980212713*5]]
    """
    """
    # no-splicing
    hyperrect = [ \
        [0.000064, 0.000080], \
        [4900000, 6900000], \
        [0.012124961140420856/5, 0.012124961140420856*5], \
        [0.017173506980212713/5, 0.017173506980212713*5]]
    # no-splicing refined 151125
    hyperrect = [ \
        [0.000069, 0.000075], \
        [5300000, 6400000], \
        [0.0082, 0.021], \
        [0.0064, 0.081]]
    # no-splicing refined 151125
    """
    
    hyperrect = trim_hyperrectangle_ranges(problem, hyperrect)
    
    hyper = []
    for ii in range(len(hyperrect)):
        hyper.append(tuple(hyperrect[ii]))
    algorithm_mc["decision_variable_ranges"] = hyper
    hyperpnts = evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals(model, problem, algorithm_mc)
    ssr = problem["confidence_region"]["ssr"]
    pnts = filter_nonlinear_confidence_region_points(hyperpnts, ssr)
    return hyperrect, pnts


def compute_nonlinear_confidence_region_intervals_and_points_extremal(model, problem, algorithm_rf, algorithm_mc, best_point):
    """
    returns solvers.monte_carlo_multiple_initial_value.ensemble_trajectoryies
    """
    intervals, points = compute_nonlinear_confidence_region_extremal_internal(model, problem, algorithm_rf, algorithm_mc, best_point)
    return intervals, points


def compute_nonlinear_confidence_region_points_extremal(model, problem, algorithm_rf, algorithm_mc, best_point):
    """
    returns solvers.monte_carlo_multiple_initial_value.ensemble_trajectoryies
    """
    _, points = compute_nonlinear_confidence_region_extremal_internal(model, problem, algorithm_rf, algorithm_mc, best_point)
    return points


def compute_nonlinear_confidence_region_intervals_extremal(model, problem, algorithm_rf, algorithm_mc, best_point):
    """
    returns list of lists
    """
    intervals, _ = compute_nonlinear_confidence_region_extremal_internal(model, problem, algorithm_rf, algorithm_mc, best_point)
    return intervals


def filter_nonlinear_confidence_region_points(hyper, cutoff):
    """
    returns solvers.monte_carlo_multiple_initial_value.ensemble_trajectoryies
    """
    hypo = copy.deepcopy(mcmiv.ensemble_trajectoryies)
    for ii in range(len(hyper["objective_function"])):
        if (check_test(hyper["objective_function"][ii], cutoff)):
            hypo["objective_function"].append(hyper["objective_function"][ii])
            hypo["decision_variables"].append(hyper["decision_variables"][ii])
    hypo["objective_function"] = numpy.array(hypo["objective_function"])
    hypo["decision_variables"] = numpy.array(hypo["decision_variables"])
    logging.debug("engine.confidence_regions.filter_nonlinear_confidence_region_points")
    logging.info("NCR hyperpoints: " + str(hypo))
    return hypo


def evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals(model, problem, algorithm):
    '''
    return numpy.array
    '''
    logging.debug("engine.confidence_regions.evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals")
    result = mcmiv.solve(model, problem, algorithm)
    points = result["succeeded"]["decision_variables"]
    ssrs = result["succeeded"]["objective_function"]
    hyper = copy.deepcopy(mcmiv.ensemble_trajectoryies)
    hyper["objective_function"] = numpy.array(ssrs)
    hyper["decision_variables"] = numpy.array(points)
    return hyper


def compute_nonlinear_confidence_intervals(model, problem, algorithm, best_point):
    mmdu.apply_decision_variables_to_parameters(best_point, model, problem)
    ssr = compute_f_constraint( \
        best_point["objective_function"],
        mmdu.get_measurement_template_for_all_experiments(problem),
        len(problem["parameter_indices"]),
        problem["confidence_region"]["confidence"])
    problem["confidence_region"]["ssr"] = ssr
    logging.info(problem["confidence_region"]["confidence"])
    logging.info(problem["confidence_region"]["ssr"])

    hyperrectangle = compute_nonlinear_confidence_hyperrectangle(model, problem, algorithm)
    return hyperrectangle


def compute_nonlinear_confidence_intervals_extremal(model, problem, algorithm, best_point):
    '''
    returns    hyperrectangle, list of list
    returns    statuses
    '''
    logging.debug("engine.confidence_regions.compute_nonlinear_confidence_intervals_extremal")
    wall_time0 = time.time()
    mmdu.apply_decision_variables_to_parameters(best_point, model, problem)
    ssr = compute_f_constraint( \
        best_point["objective_function"],
        mmdu.get_measurement_template_for_all_experiments(problem),
        len(problem["parameter_indices"]),
        problem["confidence_region"]["confidence"])
    problem["confidence_region"]["ssr"] = ssr

    hyperrectangle, statuses = compute_nonlinear_confidence_hyperrectangle_extremal(model, problem, algorithm)
    wall_time = time.time() - wall_time0

    logging.debug("engine.confidence_regions.compute_nonlinear_confidence_intervals_extremal")
    logging.info("NCR constraint " + endi.log_ssr(ssr))
    logging.info("NCR hyperrectangle bounds: " + str(hyperrectangle))
    logging.info("NCR hyperrectangle statuses: " + str(statuses))
    logging.info("NCR hyperrectangle time: " + endi.log_wall_time(wall_time))
    return hyperrectangle, statuses


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
    statuses = []
    for param_index in range(len(problem["parameter_indices"])):
        interval, status = compute_nonlinear_confidence_interval_extremal(model, problem, algorithm, param_index)
        hyperrectangle.append(interval)
        statuses.append(status)
    return hyperrectangle, statuses


# TODO: handle abnormal situations
def compute_nonlinear_confidence_interval(model, problem, algorithm, index):
    assert(problem["bounds"] is not None)
    assert(len(problem["bounds"]) == len(problem["parameter_indices"]))

    opt_model_params = copy.deepcopy(model["parameters"])
    opt_problem_params = copy.deepcopy(problem["parameters"])
    func = copy.deepcopy(problem["performance_measure"])
    args = copy.deepcopy(problem["performance_measure_args"])
    cnstrnts = copy.deepcopy(problem["constraints"])
    bounds = copy.deepcopy(problem["bounds"])
    
    problem["confidence_region"]["parameter_index"] = index
    
    problem["bounds"] = [problem["bounds"][index]]
    problem["performance_measure"] = sdo.maximise_it
    upper = sdo.solve(model, problem, algorithm)
    problem["performance_measure"] = sdo.minimise_it
    lower = sdo.solve(model, problem, algorithm)

    if (upper.status > 0 or lower.status > 0):
        codi.print_warning_error_code_message()
        # log as well

    model["parameters"] = opt_model_params
    problem["parameters"] = opt_problem_params
    problem["performance_measure"] = func
    problem["performance_measure_args"] = args
    problem["constraints"] = cnstrnts
    problem["bounds"] = bounds

    return [lower.x[0], upper.x[0]]


def maximise_distance_upper(x, x0, index):
    delta = (-1) * (x[index] - x0[index])
    return delta


def maximise_distance_lower(x, x0, index):
    delta = (x[index] - x0[index])
    return delta


def compute_nonlinear_confidence_interval_extremal(model, problem, algorithm, index):
    assert(problem["bounds"] is not None)
    assert(len(problem["bounds"]) == len(problem["parameter_indices"]))

    opt_model_params = copy.deepcopy(model["parameters"])
    opt_problem_params = copy.deepcopy(problem["parameters"])
    func = copy.deepcopy(problem["performance_measure"])
    args = copy.deepcopy(problem["performance_measure_args"])
    cnstrnts = copy.deepcopy(problem["constraints"])
    bounds = copy.deepcopy(problem["bounds"])
    
    problem["confidence_region"]["parameter_index"] = index

    # form objective function
    problem["performance_measure"] = maximise_distance_upper
    p0 = copy.deepcopy(problem["parameters"])
    problem["performance_measure_args"] = tuple([p0, index])

    # forming constraints here as this is the right level of abstraction
    # copy existing constraints back
    problem["constraints"] = form_constraints(model, problem)

    # form bounds
    bound = list(bounds[index])
    bound[0] = problem["parameters"][index]
    problem["bounds"][index] = tuple(bound)
    
    # form initial guesses
    # TODO: the algorithm has been shown to be sensitive to these
    algorithm["initial_guesses"] = numpy.asarray(problem["parameters"]) * 1

    upper = sdo.solve_std(model, problem, algorithm)
    logging.info(upper)
    if upper.status > 0 and upper.x[index] > bound[1]:
        upper.x[index] = bound[1]

    model["parameters"] = copy.deepcopy(opt_model_params)
    problem["parameters"] = copy.deepcopy(opt_problem_params)

    # form objective function
    problem["performance_measure"] = maximise_distance_lower
    # maintain arguments
    
    # forming constraints here as this is the right level of abstraction
    # copy existing constraints back
    problem["constraints"] = form_constraints(model, problem)
    
    # form bounds
    bound = list(bounds[index])
    bound[1] = problem["parameters"][index]
    problem["bounds"][index] = tuple(bound)
    
    # form initial guesses
    # TODO: the algorithm has been shown to be sensitive to these
    algorithm["initial_guesses"] = numpy.asarray(problem["parameters"]) * 1
    
    lower = sdo.solve_std(model, problem, algorithm)
    logging.info(lower)
    if lower.status > 0 and lower.x[index] < bound[0]:
        lower.x[index] = bound[0]

    # TODO: think how best to lead with this situation
    if (upper.status > 0 or lower.status > 0):
        codi.print_warning_error_code_message()
        # log as well
        # TODO: perhaps should ensure that SSR is correct

    model["parameters"] = opt_model_params
    problem["parameters"] = opt_problem_params
    problem["performance_measure"] = func
    problem["performance_measure_args"] = args
    problem["constraints"] = cnstrnts
    problem["bounds"] = bounds

    #codi.write_info(upper.status)
    #codi.write_info(lower.status)
    return [lower.x[index], upper.x[index]], [lower.status, upper.status]


# unit-tested
def likelihood_constraint(x, model_data, problem_data, ssr_0):
    assert(len(x) == len(problem_data["parameters"]))
    assert(problem_data["confidence_region"]["performance_measure"] is not None)

    mmdu.apply_values_to_parameters(x, model_data, problem_data)
    ssr = problem_data["confidence_region"]["performance_measure"](None, model_data, problem_data)
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


# TODO: should one ideally extract the calculate number of observations?
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
    logging.info("Ellipsoid: \n" + str(std_cov_matrix))
    return std_cov_matrix


"""
Best point is to compute local parameteric sensitivities and to calculate
the estimated variance based on the optimum SSR
"""
def compute_linearised_confidence_intervals(config, best_point):
    """
    best_point: models.model_data.optimisation_problem_point
    return: list of list (list of intervals)
    """
    workflow_results = wopr.do_sensitivity_based_workflow_at_solution_point(config, best_point)
    intervals = workflow_results["conf_intvs"]
    nominal = best_point["decision_variables"]
    hyperrectangle = []
    for ii in range(len(intervals)):
        hyperrectangle.append([nominal[ii]-intervals[ii], nominal[ii]+intervals[ii]])
    logging.info("Confidence intervals: \n" + str(intervals))
    logging.info("Confidence hyperrectangle: \n" + str(hyperrectangle))
    return hyperrectangle
