
import math
import numpy

def residuals(parameters, independent, function, measured):
    res = measured - function(parameters, independent)
    return res


def sum_squared_residuals(parameters, independent, function, measured):
    return math.fsum(res**2 for res in residuals(parameters, independent, function, measured))


def sum_absolute_value_residuals(values):
    return math.fsum([math.fabs(value) for value in values])


# TODO: use indices in problem instance to single-out problem-specific output structure
def residuals_st(model, model_instance, problem_instance):
    series = 0
    outputs = numpy.asarray(problem_instance["outputs"])
    inputs = numpy.asarray(problem_instance["inputs"])
    assert(outputs.shape[series] == inputs.shape[series])
    
    # TODO: generalise
    variable = 0
    res = numpy.empty(problem_instance["outputs"].shape[series])
    for ii in range(problem_instance["outputs"].shape[series]):
        measured = outputs.take(ii, axis=series)
        predicted = model(model_instance["parameters"], inputs.take(ii, axis=series))
        trajectory_m = measured[variable]
        trajectory_p = predicted[variable]
        res[ii] = numpy.subtract(trajectory_m, trajectory_p)
    return res


# TODO: use indices in problem instance to single-out problem-specific output structure
def sum_squared_residuals_st(dof, model, model_instance, problem_instance):
    assert(len(dof) == len(problem_instance["parameter_indices"]))

    # TODO: more pythonic
    if len(problem_instance["parameter_indices"]) > 0:
        for ii in range(len(dof)):
            index = problem_instance["parameter_indices"][ii]
            problem_instance["parameters"][index] = dof[ii]

    # always keep in sync
    model_instance["parameters"] = problem_instance["parameters"]
    return math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance))
