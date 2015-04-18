
import numpy

import metrics.ordinary_differential
import models.model_data as momoda


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    
    dx_dt = p * u - x
    return dx_dt


def do_setup(times):
    model_instance = dict(momoda.model_structure)
    model_instance["model"] = linear_2p2s_mock
    model_instance["parameters"] = numpy.array([1.0, 2.0])
    model_instance["inputs"] = numpy.array([1.0, 2.0])
    model_instance["states"] = numpy.array([10.0, 8.0])
    model_instance["time"] = 0.0
    
    problem_instance = dict(momoda.problem_structure)
    problem_instance["initial_conditions"] = numpy.array([10.0, 8.0])
    if times is not None:
        problem_instance["time"] = times
    problem_instance["parameters"] = numpy.array([1.0, 2.0])
    problem_instance["parameter_indices"] = numpy.array([0, 1])
    problem_instance["inputs"] = numpy.array([1.0, 2.0])
    problem_instance["performance_measure"] = metrics.ordinary_differential.sum_squared_residuals
    
    return model_instance, problem_instance