
import common.diagnostics as cd
import models.model_data as mmd
import setups.setup_data_utils as ssdu
import workflows.protocols as wpr
import workflows.workflow_data_utils as wwdu

import copy
import logging
import numpy
import time

import engine.confidence_regions as encore
import engine.diagnostics as endi
import results.plot_combinatorial as replco


baseline = {
    "point": dict(mmd.optimisation_problem_point),
    "of_delta": 0.0,
    "dv_deltas" : [],
    }


calib_valid_baseline = {
    "calib": copy.deepcopy(baseline),
    "valid": copy.deepcopy(baseline),
    }


# self.do_experiment_setup
def test_baseline_calibration(setup, baseline, unittester):
    """
    Does calibration, and then basic and sensitivity workflows at solution point 
    baseline    testpoint, can be None
    return      return: models.model_data.optimisation_problem_point
    """
    config = setup()
    calibrated = wpr.do_calibration_and_compute_performance_measure(config)
    # output
    if True:
        cd.print_decision_variables_and_objective_function(calibrated)
        post_proc = wpr.do_basic_workflow_at_solution_point(config, calibrated)
        wwdu.print_system_based_point_results(post_proc)
        post_proc = wpr.do_sensitivity_based_workflow_at_solution_point(config, calibrated)
        wwdu.print_sensitivity_based_point_results(post_proc)
    # test
    if baseline is not None:
        actual = calibrated["objective_function"]
        expected = baseline["point"]["objective_function"]
        unittester.assertAlmostEquals(actual, expected, delta=baseline["of_delta"])
        # test
        actual = calibrated["decision_variables"]
        expected = baseline["point"]["decision_variables"]
        deltas = baseline["dv_deltas"]
        [unittester.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]
    else:
        cd.print_unexpected_code_branch_message()
    return calibrated


# self.do_experiment_setup
def test_baseline_validation(setup, baseline, unittester, point):
    """
    baseline can be None
    """
    config = setup()
    # TODO: should probably be returning here if there is no validation to perform
    # e.g., in order to plot calib and valid
    # WIP 2015-06-20; this is buggy, it should be set higher up and or checked for correctness
    ssdu.set_next_protocol_step(config)
    validated = wpr.do_validation_and_compute_performance_measure_at_solution_point(config, point)
    # output
    if True:
        cd.print_decision_variables_and_objective_function(validated)
        post_proc = wpr.do_basic_workflow_at_solution_point(config, validated)
        wwdu.print_system_based_point_results(post_proc)
        post_proc = wpr.do_sensitivity_based_workflow_at_solution_point(config, validated)
        wwdu.print_sensitivity_based_point_results(post_proc)
    # test
    if baseline is not None:
        actual = validated["objective_function"]
        expected = baseline["point"]["objective_function"]
        unittester.assertAlmostEquals(actual, expected, delta=baseline["of_delta"])
        # test
        actual = validated["decision_variables"]
        expected = baseline["point"]["decision_variables"]
        deltas = baseline["dv_deltas"]
        [unittester.assertAlmostEquals(act, exp, delta=diff) for act, exp, diff in zip(actual, expected, deltas)]
    else:
        cd.print_unexpected_code_branch_message()
    return validated


def test_baseline_calibration_and_validation(setup, baseline, unittester):
    # there is no good reason why this should be different
    refpoint = baseline["calib"]
    basepoint = baseline["valid"]
    basepoint["point"]["decision_variables"] = refpoint["point"]["decision_variables"]
    basepoint["of_delta"] = refpoint["of_delta"]
    basepoint["dv_deltas"] = refpoint["dv_deltas"]

    calibrated = test_baseline_calibration(setup, baseline["calib"], unittester)
    test_baseline_validation(setup, baseline["valid"], unittester, calibrated)
    return calibrated


# TODO: extract to protocol
def test_calibration_with_nonlinear_confidence_region(protocol, baseline, unittester):
    """
    protocol setup_data.experiment_protocol
    """
    # pre-conditions
    assert(len(protocol["steps"]) == 2)
    
    nlr = 0
    mcs = 1

    # do regression/calibration
    best_point = wpr.do_calibration_and_compute_performance_measure(protocol["steps"][nlr])
    
    unittester.assertAlmostEquals( \
        best_point["objective_function"], baseline["objective_function"])
    [unittester.assertAlmostEquals(act, exp, delta=eps) for act, exp, eps in zip( \
        numpy.asarray(best_point["decision_variables"]).flatten(), \
        numpy.asarray(baseline["decision_variables"]).flatten(), \
        numpy.asarray(baseline["decision_variables_eps"]).flatten())]
    
    # setup nonlin conf reg
    algorithm_nlr = protocol["steps"][nlr]["algorithm_setup"](None)
    model, problem, algorithm_mcs = ssdu.get_model_problem_algorithm_with_calib(protocol["steps"][mcs])
    # WIP: 2015-07-16; rework
    if True:
        do_appy_bounds(best_point["decision_variables"], problem)
    problem["decision_variables"] = best_point["decision_variables"]
    
    # do nonlin conf reg
    wall_time0 = time.time()
    actual_intervals, actual_points = encore.compute_nonlinear_confidence_region_intervals_and_points_extremal( \
        model, problem, algorithm_nlr, algorithm_mcs, best_point)
    wall_time = time.time() - wall_time0
    number_of_points = len(numpy.transpose(actual_points["objective_function"]))

    # logging
    logging.info("best point: " + str(best_point))
    logging.info("ncr intervals: " + str(actual_intervals))
    logging.info("bounds: " + str(problem["bounds"]))
    logging.info(endi.log_points(actual_points))
    logging.info(endi.log_wall_time(wall_time))
    logging.info(endi.log_number_of_trials(algorithm_mcs["number_of_trials"]))
    logging.info(endi.log_number_of_points(number_of_points))
    
    # testing
    if baseline is not None:
        expected = baseline["intervals"]
        [unittester.assertAlmostEquals(act, exp, 8) for act, exp in zip( \
            numpy.asarray(actual_intervals).flatten(), numpy.asarray(expected).flatten())]
        unittester.assertEquals(number_of_points, baseline["number_of_points"])
    else:
        cd.print_unexpected_code_branch_message()
    
    # plot nonlin conf reg
    if protocol["steps"][mcs]["local_setup"]["do_plotting"]:
        replco.plot_combinatorial_region_projections(numpy.transpose(actual_points["decision_variables"]))


# TODO: move out
def do_appy_bounds(nominal, problem):
    lf = 1E-2
    uf = 1E+2
    problem["bounds"] = [ \
        (nominal[0]*lf,nominal[0]*uf), \
        (nominal[1]*lf,nominal[1]*uf), \
        (nominal[2]*lf,nominal[2]*uf), \
        (nominal[3]*lf,nominal[3]*uf)]


def test_calibration_with_linearised_confidence_region(config, baseline, unittester):
    best_point = wpr.do_calibration_and_compute_performance_measure(config)
    assert(baseline is not None)

    unittester.assertAlmostEquals( \
        best_point["objective_function"], baseline["objective_function"])
    [unittester.assertAlmostEquals(act, exp, delta=eps) for act, exp, eps in zip( \
        numpy.asarray(best_point["decision_variables"]).flatten(), \
        numpy.asarray(baseline["decision_variables"]).flatten(), \
        numpy.asarray(baseline["decision_variables_eps"]).flatten())]
    
    # intervals and ellipsoid
    intervals = encore.compute_linearised_confidence_intervals(config, best_point)
    ellipsoid = encore.compute_linearised_confidence_region_ellipsoid(config, best_point)

    # testing
    expected = baseline["intervals"]
    [unittester.assertAlmostEquals(act, exp, 8) for act, exp in zip(numpy.asarray(intervals).flatten(), numpy.asarray(expected).flatten())]
    expected = baseline["ellipsoid"]
    diff = baseline["delta"]
    [unittester.assertAlmostEquals(act, exp, delta=eps) for act, exp, eps in zip( \
        numpy.asarray(ellipsoid).flatten(), numpy.asarray(expected).flatten(), numpy.asarray(diff).flatten())]
    
    # plot lin conf reg
    if config["local_setup"]["do_plotting"]:
        replco.plot_combinatorial_ellipsoid_projections(best_point['decision_variables'], ellipsoid)