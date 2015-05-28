
import numpy

import metrics.ordinary_differential as meordi
import models.model_data as momoda


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    
    dx_dt = p * u - x
    return dx_dt


def do_setup(times):
    """
    times:     can be None
    return:    model and problem
    """
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
    problem_instance["performance_measure"] = meordi.sum_squared_residuals
    
    problem_instance["output_indices"] = [0, 1]
    
    return model_instance, problem_instance


def do_model():
    model_instance = dict(momoda.model_structure)
    model_instance["model"] = linear_2p2s_mock
    model_instance["parameters"] = numpy.array([1.0, 2.0])
    model_instance["inputs"] = numpy.array([1.0, 2.0])
    model_instance["states"] = numpy.array([10.0, 8.0])
    model_instance["time"] = 0.0
    return model_instance
    
    
def do_problem(dummy1, dummy2):
    problem_instance = dict(momoda.problem_structure)
    problem_instance["initial_conditions"] = numpy.array([10.0, 8.0])
    problem_instance["time"] = numpy.arange(10)
    problem_instance["parameters"] = numpy.array([1.0, 2.0])
    problem_instance["parameter_indices"] = numpy.array([0, 1])
    problem_instance["inputs"] = numpy.array([1.0, 2.0])
    problem_instance["performance_measure"] = meordi.sum_squared_residuals
    problem_instance["output_indices"] = [0, 1]
    
    problem_instance["output_filters"] = dict(momoda.output_filters)
    problem_instance["output_filters"]["calibration_mask"] = [5]
    problem_instance["output_filters"]["validation_mask"] = [0,5]
    
    return problem_instance

    
def do_data():
    data = dict(momoda.calib_valid_experimental_dataset)
    calib = dict(momoda.experimental_dataset)
    calib["time"] = numpy.arange(5)
    calib["observables"] = [numpy.arange(5), numpy.arange(5)]
    valid = dict(momoda.experimental_dataset)
    valid["time"] = numpy.arange(5,10)
    valid["observables"] = [numpy.arange(5,10), numpy.arange(5,10)]
    data["id"] = "mock"
    data["calib"] = calib
    data["valid"] = valid
    return data


def do_experiment():
    config = {}
    config["model_setup"] = do_model
    config["data_setup"] = do_data
    config["problem_setup"] = do_problem
    return config
