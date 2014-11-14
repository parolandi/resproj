
import copy
import numpy

import data.experimental_data_splicing as deds
import data.generator
import experiments.protocol_data as epd
import metrics.ordinary_differential as mod
import models.model_data
import setups.setup_data
import solvers.initial_value


def do_model_setup():
    inputs = numpy.array([1.0, 2.0])
    params = numpy.array([1.0, 2.0])
    states = numpy.array([10.0, 8.0])
    
    # boiler-plate
    model_instance = dict(models.model_data.model_structure)
    model_instance["inputs"] = inputs
    model_instance["parameters"] = params
    model_instance["states"] = states
    model_instance["time"] = 0.0
    model_instance["model"] = models.ordinary_differential.linear_2p2s
    return model_instance


def do_problem_setup(model_data, data_instance):
    assert(model_data is not None)
    assert(data_instance is not None)
    
    problem_data = dict(models.model_data.problem_structure)
    problem_data["initial_conditions"] = copy.deepcopy(model_data["states"])
    problem_data["time"] = data_instance["time"]
    problem_data["parameters"] = copy.deepcopy(model_data["parameters"])
    problem_data["inputs"] = copy.deepcopy(model_data["inputs"])

    problem_data["performance_measure"] = mod.sum_squared_residuals_st
    problem_data["parameter_indices"] = numpy.array([0, 1])
    # WIP:
    problem_data["parameters"] = numpy.zeros(len(problem_data["parameter_indices"]))
#    problem_data["parameters"] = numpy.array([1.0, 2.0])
    
    for ii in range(len(problem_data["parameter_indices"])):
        problem_data["parameters"][ii] = copy.deepcopy(model_data["parameters"][problem_data["parameter_indices"][ii]])
    
#    problem_data["bounds"] = [(0,None), (0,None), (0,None), (0,None), (0,None)]
    
    problem_data["output_indices"] = numpy.array([0, 1])
    problem_data["outputs"] = data_instance["observables"]
    assert(len(["output_indices"]) == len(["outputs"]))

    problem_data["initial"] = "exclude"

    return problem_data


def do_sensitivity_model_setup():
    inputs = numpy.array([1.0, 2.0])
    params = numpy.array([1.0, 2.0])
    sys_and_sens_states = numpy.array([10.0, 8.0, 0.0, 0.0, 0.0, 0.0])
    
    # boiler-plate
    model_instance = dict(models.model_data.model_structure)
    model_instance["inputs"] = inputs
    model_instance["parameters"] = params
    model_instance["states"] = sys_and_sens_states
    model_instance["time"] = 0.0
    model_instance["model"] = models.ordinary_differential.state_and_sensitivities_linear_2p2s
    return model_instance


# TODO: DRY
def do_sensitivity_problem_setup(model_data, data_instance):
    assert(model_data is not None)
    assert(data_instance is not None)
    
    problem_data = dict(models.model_data.problem_structure)
    problem_data["initial_conditions"] = copy.deepcopy(model_data["states"])
    problem_data["time"] = data_instance["time"]
    problem_data["parameters"] = copy.deepcopy(model_data["parameters"])
    problem_data["inputs"] = copy.deepcopy(model_data["inputs"])

    problem_data["output_indices"] = numpy.array([0, 1])
    problem_data["outputs"] = data_instance["observables"]
    assert(len(["output_indices"]) == len(["outputs"]))

    problem_data["initial"] = "exclude"

    return problem_data


# TODO: DRY
def do_baseline_data_setup():
    # configuration
    final_time = 3.0
    intervals = 30
    stdev = 0.2
    
    times = numpy.linspace(0.0, final_time, intervals+1, endpoint=True)
    inputs = numpy.array([1.0, 2.0])
    params = numpy.array([1.0, 2.0])
    param_indices = numpy.array([0, 1])
    states = numpy.array([10.0, 8.0])
    
    # boiler-plate
    model_instance = dict(models.model_data.model_structure)
    model_instance["inputs"] = inputs
    model_instance["parameters"] = params
    model_instance["states"] = states
    model_instance["time"] = 0.0
    
    problem_instance = dict(models.model_data.problem_structure)
    problem_instance["initial_conditions"] = copy.deepcopy(model_instance["states"])
    problem_instance["inputs"] = copy.deepcopy(model_instance["inputs"])
    problem_instance["time"] = times
    problem_instance["parameters"] = copy.deepcopy(model_instance["parameters"])
    problem_instance["parameter_indices"] = param_indices
#    problem_instance["initial"] = "exclude"

    mi = copy.deepcopy(model_instance)
    pi = copy.deepcopy(problem_instance)

    mi["model"] = models.ordinary_differential.linear_2p2s
    measured = numpy.asarray(solvers.initial_value.compute_timecourse_trajectories(None, mi, pi))
    
    no_states = len(model_instance["states"])
    data.generator.set_seed(117)
    measurement_noise = []
    for _ in range(no_states):
        measurement_noise.append(stdev * data.generator.normal_distribution(intervals+1))
    data.generator.unset_seed()
    
    experimental = measured + measurement_noise
    
    trajectory_data = []
    trajectory_data.append(times)
    [trajectory_data.append(experimental[ii]) for ii in range(len(experimental))]
    return trajectory_data


def do_baseline_data_setup_spliced_111111():
    trajectories = do_baseline_data_setup()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111111(trajectories)
    return spliced_trajectories


def do_baseline_data_setup_spliced_111000():
    trajectories = do_baseline_data_setup()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111000(trajectories)
    return spliced_trajectories


def do_algorithm_setup(instrumentation_data):
    initial_guesses = numpy.array([1.0, 2.0])

    algorithm_data = dict(solvers.solver_data.algorithm_structure)
    if instrumentation_data is not None:
        algorithm_data["callback"] = instrumentation_data["logger"].log_decision_variables
    algorithm_data["initial_guesses"] = initial_guesses
    algorithm_data["method"] = "CG"
    return algorithm_data

    
def do_instrumentation_setup():
    instrumentation_data = dict(setups.setup_data.instrumentation_data)
    instrumentation_data["logger"] = solvers.least_squares.DecisionVariableLogger()
    return instrumentation_data


def do_protocol_setup():
    protocol_data = dict(epd.protocol_data)
    protocol_data["performance_measure"] = mod.sum_squared_residuals_st
    return protocol_data
