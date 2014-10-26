
import math
import numpy

import common.diagnostics as cd
import common.utilities
import solvers.initial_value


def handle_initial_point(values, problem_instance):
    if problem_instance["initial"] == "exclude":
        values = common.utilities.exclude_initial_point(values)
    return values


# TODO: rename; remove "_st"
# TODO: consider always returning list of residuals, even in degenerate case of single residual
def residuals_st(model, model_instance, problem_instance):
    # TODO: preconditions
    assert(len(problem_instance["output_indices"]) > 0)
    assert(len(problem_instance["output_indices"]) == len(problem_instance["outputs"]))
    
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
    # TODO: more pythonic
    if len(measured.shape) == 1:
        measured_s = measured
        predicted_s = predicted[problem_instance["output_indices"][0]]
        res = numpy.subtract(measured_s, predicted_s)
        return res
    
    res = numpy.empty(measured.shape)
    for jj in range(len(problem_instance["output_indices"])):
        measured_s = measured[jj]
        predicted_s = predicted[problem_instance["output_indices"][jj]]
        res[jj] = numpy.subtract(measured_s, predicted_s)
    return res


# TODO: rename and reuse
def residuals_dof(dof, model, model_instance, problem_instance):
    if len(problem_instance["parameter_indices"]) > 0:
        for ii in range(len(dof)):
            index = problem_instance["parameter_indices"][ii]
            model_instance["parameters"][index] = dof[ii]
            problem_instance["parameters"][ii] = dof[ii]

    if model is not None:
        model_instance["model"] = model
        cd.print_legacy_code_message()

    return residuals_st(model, model_instance, problem_instance)


# compute the ssr for each trajectory
def sums_squared_residuals(dof, model, model_instance, problem_instance):
    if len(problem_instance["parameter_indices"]) > 0:
        for ii in range(len(dof)):
            index = problem_instance["parameter_indices"][ii]
            model_instance["parameters"][index] = dof[ii]
            problem_instance["parameters"][ii] = dof[ii]

    if model is not None:
        model_instance["model"] = model
        cd.print_legacy_code_message()

    sum_res = []
    if len(problem_instance["output_indices"]) == 1:
        sum_res.append(math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance)))
        return sum_res
    for ii in range(len(problem_instance["outputs"])):
        sum_res.append(math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance)[ii]))
    return sum_res


# TODO: compute state-wise and experiment-wise
# TODO: rename; remove "_st"
# dof: a list/array or None
# TODO: test empty array
def sum_squared_residuals_st(dof, model, model_instance, problem_instance):
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

    # TODO: more pythonic
    res = 0.0
    residuals = residuals_st(model, model_instance, problem_instance)
    for ii in range(len(problem_instance["output_indices"])):
        res += math.fsum(res**2 for res in residuals[ii])
    return res
