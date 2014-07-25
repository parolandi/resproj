
import math
import numpy

def residuals(parameters, independent, function, measured):
    res = measured - function(parameters, independent)
    return res


def sum_squared_residuals(parameters, independent, function, measured):
    return math.fsum(res**2 for res in residuals(parameters, independent, function, measured))


def sum_absolute_value_residuals(values):
    return math.fsum([math.fabs(value) for value in values])


def residuals_st(model, model_instance, problem_instance):
    series = 0
    states_index = 1
    outputs = numpy.asarray(problem_instance["outputs"])
    inputs = numpy.asarray(problem_instance["inputs"])
    assert(outputs.shape[states_index] == len(problem_instance["output_indices"])) 
    assert(outputs.shape[series] == inputs.shape[series])
    
    # there is one residual per experiment
    res = numpy.empty(problem_instance["outputs"].shape)
    states = 0
    for ii in range(problem_instance["outputs"].shape[series]):
        measured = outputs.take(ii, axis=series)
        predicted = model(model_instance["parameters"], inputs.take(ii, axis=series))
        # there is one residual per state (and per experiment)
        res_s = numpy.empty(measured.shape[states])
        for jj in range(measured.shape[states]):
            measured_s = measured[jj]
            predicted_s = predicted[problem_instance["output_indices"][jj]]
            res_s[jj] = numpy.subtract(measured_s, predicted_s)
            res[ii][jj] = res_s[jj]
    return res


def sum_squared_residuals_st(dof, model, model_instance, problem_instance):
    assert(len(dof) == len(problem_instance["parameter_indices"]))

    # TODO: more pythonic
    if len(problem_instance["parameter_indices"]) > 0:
        for ii in range(len(dof)):
            index = problem_instance["parameter_indices"][ii]
            model_instance["parameters"][index] = dof[ii]
            problem_instance["parameters"][ii] = dof[ii]
    
    # TODO: more pythonic
    res = 0.0
    # TODO: compute state-wise and experiment-wise
    for ii in range(len(problem_instance["outputs"])):
        res += math.fsum(res**2 for res in residuals_st(model, model_instance, problem_instance)[ii])
    return res
