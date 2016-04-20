
import numpy

import metrics.ordinary_differential as meordi
import models.model_data as momoda
import solvers.local_sensitivities as solose
import workflows.protocol_data as woprda


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
    
    
def do_model_invariant():
    model_instance = dict(momoda.model_structure)
    model_instance["model"] = linear_2p2s_mock
    model_instance["parameters"] = numpy.array([1.0, 1.0])
    model_instance["inputs"] = numpy.array([1.0, 1.0])
    model_instance["states"] = numpy.array([1.0, 1.0])
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

    
def do_problem_invariant(dummy1, dummy2):
    problem_instance = dict(momoda.problem_structure)
    problem_instance["initial_conditions"] = numpy.array([1.0, 1.0])
    problem_instance["time"] = numpy.arange(10)
    problem_instance["parameters"] = numpy.array([1.0, 1.0])
    problem_instance["parameter_indices"] = numpy.array([0, 1])
    problem_instance["inputs"] = numpy.array([1.0, 1.0])
    problem_instance["performance_measure"] = meordi.sum_squared_residuals
    problem_instance["output_indices"] = [0, 1]
    
    problem_instance["output_filters"] = dict(momoda.output_filters)
    problem_instance["output_filters"]["calibration_mask"] = [5]
    problem_instance["output_filters"]["validation_mask"] = [0,5]
    
    return problem_instance


def do_problem_invariant_with_data(dummy1, data_instance):
    problem_instance = dict(momoda.problem_structure)
    problem_instance["initial_conditions"] = numpy.array([1.0, 1.0])
    problem_instance["time"] = numpy.arange(10)
    problem_instance["parameters"] = numpy.array([1.0, 1.0])
    problem_instance["parameter_indices"] = numpy.array([0, 1])
    problem_instance["inputs"] = numpy.array([1.0, 1.0])
    problem_instance["performance_measure"] = meordi.sum_squared_residuals
    problem_instance["output_indices"] = [0, 1]
    
    problem_instance["output_filters"] = dict(momoda.output_filters)
    problem_instance["output_filters"]["calibration_mask"] = [5]
    problem_instance["output_filters"]["validation_mask"] = [0,5]

    problem_instance["performance_observables"] = meordi.sums_squared_residuals_unlegacy

    # TODO: 2015-06-04; hack?
    assert(data_instance is not None)
    problem_instance["outputs"] = data_instance["observables"]
    assert(len(["output_indices"]) == len(["outputs"]))
    problem_instance["output_filters"]["measurement_splices"] = [slice(0, 5, 1)]

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


def do_data_invariant():
    data = dict(momoda.calib_valid_experimental_dataset)
    calib = dict(momoda.experimental_dataset)
    calib["time"] = numpy.arange(5)
    calib["observables"] = [numpy.ones(5), numpy.ones(5)]
    valid = dict(momoda.experimental_dataset)
    valid["time"] = numpy.arange(5,10)
    valid["observables"] = [numpy.ones(5), numpy.ones(5)]
    data["id"] = "mock"
    data["calib"] = calib
    data["valid"] = valid
    return data


def do_experiment():
    config = {}
    config["model_setup"] = do_model
    config["data_setup"] = do_data
    config["problem_setup"] = do_problem
    config["protocol_setup"] = do_protocol
    return config


def do_experiment_invariant():
    config = {}
    config["model_setup"] = do_model_invariant
    config["data_setup"] = None
    config["problem_setup"] = do_problem_invariant
    return config


def do_experiment_with_protocol_as_invariant():
    #reducing dependencies
    config = {}
    config["protocol_step"] = {}
    
    config["model_setup"] = do_model_invariant
    config["data_setup"] = do_data_invariant
    config["problem_setup"] = do_problem_invariant_with_data
    config["protocol_setup"] = do_protocol
    config["protocol_step"]["calib"] = "do"
    config["protocol_step"]["valid"] = "do"
    return config


def do_experiment_with_protocol_and_sensitivities_as_invariant():
    #reducing dependencies
    config = {}
    config["protocol_step"] = {}
    
    config["model_setup"] = do_model_invariant
    config["data_setup"] = do_data_invariant
    config["problem_setup"] = do_problem_invariant_with_data
    config["protocol_setup"] = do_protocol
    config["protocol_step"]["calib"] = "do"
    config["protocol_step"]["valid"] = "do"
    config["sensitivity_setup"] = do_forward_sensitivity_setup()
    return config


def do_forward_sensitivity_setup():
    return solose.compute_timecourse_trajectories_and_sensitivities


def do_protocol():
    protocol_data = dict(woprda.protocol_data)
    protocol_data["performance_measure"] = meordi.sum_squared_residuals
    return protocol_data


# TODO: 2015-06-22; does it make sense to avoid this dependency?
def get_model_data_problem(config):
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["calib"])
    return model_instance, data_instance, problem_instance
