
import math
import numpy

import common.diagnostics as cd
import common.utilities
import models.model_data_utils as mmdu

import engine.state_integration as enstin
# legacy
import solvers.initial_value


def handle_initial_point(values, problem_instance):
    if problem_instance["initial"] == "exclude":
        values = common.utilities.exclude_initial_point(values)
    return values


# TODO: 2015-05-28; should always return a list
def residuals(model, problem):
    """
    compute residuals for individual measurements for all experiments
    returns real or numpy.array
    """
    num_exps = len(problem["experiments"])
    if num_exps == 0:
        # this could return a real and should not
        if problem["output_filters"] is None:
            return residuals_st(None, model, problem)
        else:
            return residuals_single_experiment(model, problem)
    residuals_per_exp = []
    for ii in range(num_exps):
        # TODO: extend to handle forcing_inputs too
        # WIP: 2015-05-14, 2015-05-15
        experiment = problem["experiments"][ii]
        problem["time"] = experiment["time"]
        problem["initial_conditions"] = experiment["initial_condition_measurements"]
        problem["inputs"] = experiment["input_measurements"]
        problem["outputs"] = experiment["output_measurements"]
        res = None
        if problem["output_filters"] is None:
            res = residuals_st(None, model, problem)
        else:
            res = residuals_single_experiment(model, problem)
        residuals_per_exp.append(res)
    residuals_per_obs = []
    num_obs = len(problem["output_indices"])
    for jj in range(num_obs):
        residuals_per_obs.append(residuals_per_exp[0][jj])
    for ii in range(1,num_exps):
        for jj in range(num_obs):
            residuals_per_obs[jj] = numpy.concatenate((residuals_per_obs[jj],residuals_per_exp[ii][jj]))
    return residuals_per_obs


def sum_squared_residuals(dof, model, problem):
    """
    compute a single ssr for all observables collectively, for all experiments
    dof        values of decision variables (degrees-of-freedom); it can be None
    returns    real
    """
    if dof is not None:
        mmdu.apply_values_to_parameters(dof, model, problem)
    # MAYDO: this could be more pythonic?
    res = 0.0
    resids = residuals(model, problem)
    for ii in range(len(problem["output_indices"])):
        res += math.fsum(res**2 for res in resids[ii])
    return res


# TODO: 2015-05-18, more pythonic
# TODO: 2015-05-28; should always return a list
def residuals_single_experiment(model, problem):
    """
    compute residuals for individual measurements for a single experiment
    returns real or numpy.array
    """
    assert(model is not None and problem is not None)
    assert(len(problem["output_indices"]) > 0)
    assert(len(problem["output_indices"]) == len(problem["outputs"]))
    # TODO: preconditions
    
    #TODO: handle initial point?
    measured = numpy.asarray(problem["outputs"])
    predicted = enstin.compute_timecourse_trajectories(model, problem)
    if problem["measurements_covariance_trace"] is None:
        cov = numpy.ones(len(problem["outputs"]))
    else:
        cov = problem["measurements_covariance_trace"] 

    if len(measured.shape) == 1:
        assert(False)
        raise
    # there is one residual per experiment
    # but for the moment there is also a single experiment
    # there is one residual per state (and per experiment)
    res = numpy.empty(measured.shape)
    for jj in range(len(problem["output_indices"])):
        measured_s = measured[jj]
        predicted_s = predicted[problem["output_indices"][jj]]
        assert(len(measured_s) == len(predicted_s))
        res[jj] = numpy.subtract(measured_s, predicted_s) / cov[jj]
    return res


def sums_squared_residuals_unlegacy(model, problem):
    """
    compute the ssr for each observable (trajectory) independently, for all experiments
    returns numpy.array
    """
    # TODO: preconditions
    
    sum_res = []
    ress = residuals(model, problem)
    for ii in range(len(problem["output_indices"])):
        sum_res.append(math.fsum(res**2 for res in ress[ii]))
    return numpy.asarray(sum_res)


# -----------------------------------------------------------------------------
'''
Legacy
'''
# -----------------------------------------------------------------------------

# TODO: rename; remove "_st"
# TODO: !! consider always returning list of residuals, even in degenerate case of single residual
def residuals_st(model, model_instance, problem_instance):
    """
    compute residuals for individual measurements for a single experiment
    returns real or list (should always return a list)
    """
    assert(len(problem_instance["output_indices"]) > 0)
    assert(len(problem_instance["output_indices"]) == len(problem_instance["outputs"]))
    # TODO: preconditions
    
    if model is not None:
        model_instance["model"] = model
        cd.print_legacy_code_message()
    
    #TODO: here an in initial value?
    measured = handle_initial_point(numpy.asarray(problem_instance["outputs"]), problem_instance)
    
    predicted = solvers.initial_value.compute_timecourse_trajectories( \
        model, model_instance, problem_instance)

    # there is one residual per experiment
    # but for the moment there is also a single experiment
    # there is one residual per state (and per experiment)
    res = 0
    if problem_instance["measurements_covariance_trace"] is None:
        cov = numpy.ones(len(problem_instance["outputs"]))
    else:
        cov = problem_instance["measurements_covariance_trace"] 
    # TODO: more pythonic
    if len(measured.shape) == 1:
        measured_s = measured
        predicted_s = predicted[problem_instance["output_indices"][0]]
        res = numpy.subtract(measured_s, predicted_s) / cov[0]
        return res
    
    res = numpy.empty(measured.shape)
    for jj in range(len(problem_instance["output_indices"])):
        measured_s = measured[jj]
        predicted_s = predicted[problem_instance["output_indices"][jj]]
        res[jj] = numpy.subtract(measured_s, predicted_s) / cov[jj]
    return res


# TODO: rename and reuse; residuals at point
def residuals_dof(dof, model, model_instance, problem_instance):
    assert(False)
    """
    It has side effects on model_instance and problem_instance
    """
    if len(problem_instance["parameter_indices"]) > 0:
        for ii in range(len(dof)):
            index = problem_instance["parameter_indices"][ii]
            model_instance["parameters"][index] = dof[ii]
            problem_instance["parameters"][ii] = dof[ii]

    if model is not None:
        model_instance["model"] = model
        cd.print_legacy_code_message()

    return residuals_st(model, model_instance, problem_instance)


def sums_squared_residuals(dof, model, model_instance, problem_instance):
    """
    compute the ssr for each observable (trajectory) independently
    returns list
    """
    if dof is not None:
        assert(len(dof) == len(problem_instance["parameter_indices"]))
    # TODO: preconditions
    # TODO: more pythonic
    
    if dof is not None:
        for ii in range(len(dof)):
            index = problem_instance["parameter_indices"][ii]
            model_instance["parameters"][index] = dof[ii]
            problem_instance["parameters"][ii] = dof[ii]

    if model is not None:
        model_instance["model"] = model
        cd.print_legacy_code_message()

    sum_res = []
    # TODO: tidy-up
    if len(problem_instance["output_indices"]) == 1:
        sum_res.append(math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance)))
        return sum_res
    for ii in range(len(problem_instance["outputs"])):
        sum_res.append(math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance)[ii]))
    return sum_res


# TODO: rename; remove "_st"
# dof: a list/array or None
# TODO: test empty array
def sum_squared_residuals_st(dof, model, model_instance, problem_instance):
    """
    compute a single ssr for all observables collectively
    returns real
    """
    if dof is not None:
        assert(len(dof) == len(problem_instance["parameter_indices"]))
    # TODO: preconditions
    
    if dof is not None:
        mmdu.apply_values_to_parameters(dof, model_instance, problem_instance)
    
    if model is not None:
        model_instance["model"] = model
        cd.print_legacy_code_message()

    # TODO: more pythonic
    res = 0.0
    residuals = residuals_st(model, model_instance, problem_instance)
    for ii in range(len(problem_instance["output_indices"])):
        res += math.fsum(res**2 for res in residuals[ii])
    return res
