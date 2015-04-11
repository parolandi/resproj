
import copy
import numpy

import data.experimental_data_splicing as deds
import data.generator
import workflows.protocol_data as wpd
import metrics.ordinary_differential as mod
import models.model_data
import models.model_data_utils as mmdu
import models.ordinary_differential
import setups.setup_data
import solvers.initial_value
import solvers.solver_utils as sosout


def do_abstract_model_setup():
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


# TODO: obsolete; now _lin()
def do_model_setup():
    return do_abstract_model_setup()


def do_model_setup_lin():
    return do_abstract_model_setup()


def do_model_setup_nonlin():
    model_instance = do_abstract_model_setup()
    model_instance["model"] = models.ordinary_differential.nonlinear_2p2s
    return model_instance


def do_model_setup_nonlin_in_params():
    model_instance = do_abstract_model_setup()
    model_instance["model"] = models.ordinary_differential.nonlinear_in_params_2p2s
    return model_instance

# -----------------------------------------------------------------------------

# TODO: consider adding bounds?
# TODO: rename to abstract
def do_base_problem_setup(model_data, data_instance):
    """
    data_instance calib_valid_experimental_dataset["calib"]
    """
    assert(model_data is not None)
    
    problem_data = dict(models.model_data.problem_structure)
    problem_data["initial_conditions"] = copy.deepcopy(model_data["states"])
    if data_instance is not None:
        problem_data["time"] = data_instance["time"]
    problem_data["parameters"] = copy.deepcopy(model_data["parameters"])
    problem_data["inputs"] = copy.deepcopy(model_data["inputs"])

    problem_data["performance_measure"] = mod.sum_squared_residuals_st
    problem_data["confidence_region"]["performance_measure"] = mod.sum_squared_residuals_st
    problem_data["parameter_indices"] = numpy.array([0, 1])
    problem_data["parameters"] = numpy.zeros(len(problem_data["parameter_indices"]))
    
    # TODO: re-use other mechanisms
    for ii in range(len(problem_data["parameter_indices"])):
        problem_data["parameters"][ii] = copy.deepcopy(model_data["parameters"][problem_data["parameter_indices"][ii]])
    
    problem_data["output_indices"] = numpy.array([0, 1])
    if data_instance is not None:
        problem_data["outputs"] = data_instance["observables"]
        assert(len(["output_indices"]) == len(["outputs"]))

    problem_data["initial"] = "exclude"

    problem_data["bounds"] = [(-10,10), (-10,10)]

    return problem_data


def do_problem_setup_without_covariance(model_data, data_instance):
    return do_base_problem_setup(model_data, data_instance)


def do_problem_setup_with_covariance(model_data, data_instance):
    problem_data = do_base_problem_setup(model_data, data_instance)
    problem_data["measurements_covariance_trace"] = numpy.ones(2)
    mmdu.check_correctness_of_measurements_covariance_matrix(problem_data)
    return problem_data

#-----------------------------------------------------------------------------#

def do_abstract_sensitivity_model_setup():
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


def do_sensitivity_model_setup_lin():
    model_instance = do_abstract_sensitivity_model_setup()
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

    problem_data["parameter_indices"] = numpy.array([0, 1])
    
    problem_data["output_indices"] = numpy.array([0, 1])
    problem_data["outputs"] = data_instance["observables"]
    assert(len(["output_indices"]) == len(["outputs"]))

    return problem_data

# -----------------------------------------------------------------------------

#TODO: this could be config
#TODO: timecourse_simulation
def do_abstract_data_setup(model, problem, covariance_trace):
    """
    return list (of trajectory data)
    """
    # configuration
    final_time = 3.0
    intervals = 30
    
    times = numpy.linspace(0.0, final_time, intervals+1, endpoint=True)
    model_instance = model()
    model_instance["time"] = 0.0
    problem_instance = problem(model_instance, None)
    problem_instance["time"] = times
    problem_instance["initial"] = "include"
    mi = copy.deepcopy(model_instance)
    pi = copy.deepcopy(problem_instance)

    measured = numpy.asarray(solvers.initial_value.compute_timecourse_trajectories(None, mi, pi))
    # TODO: BUG, this only works for identical observables and states!
    no_states = len(model_instance["states"])
    data.generator.set_seed(117)
    measurement_noise = []
    for ii in range(no_states):
        st_dev = covariance_trace[ii]
        measurement_noise.append(st_dev * data.generator.normal_distribution(intervals+1))
    data.generator.unset_seed()
    experimental = measured + measurement_noise
    
    trajectory_data = []
    trajectory_data.append(times)
    [trajectory_data.append(experimental[ii]) for ii in range(len(experimental))]
    return trajectory_data


def do_baseline_data_setup(covariance_trace):
    return do_abstract_data_setup(do_model_setup, do_base_problem_setup, covariance_trace)


def do_baseline_data_setup_with_covariance():
    return do_baseline_data_setup(numpy.array([0.2, 0.2]))
    

def do_baseline_data_setup_without_covariance():
    return do_baseline_data_setup(numpy.array([1.0, 1.0]))


def do_baseline_data_setup_spliced_111111():
    """with covariance"""
    """ returns: calib_valid_experimental_dataset """
    trajectories = do_baseline_data_setup_with_covariance()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111111(trajectories)
    return spliced_trajectories


def do_baseline_data_setup_spliced_111111_without_covariance():
    trajectories = do_baseline_data_setup_without_covariance()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111111(trajectories)
    return spliced_trajectories


def do_baseline_data_setup_spliced_111000():
    trajectories = do_baseline_data_setup_with_covariance()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111000(trajectories)
    return spliced_trajectories



def do_data_setup_nonlin(covariance_trace):
    return do_abstract_data_setup(do_model_setup_nonlin, do_base_problem_setup, covariance_trace)


def do_data_setup_nonlin_without_covariance():
    return do_data_setup_nonlin(numpy.array([1.0, 1.0]))


def do_data_setup_nonlin_spliced_111111_without_covariance():
    trajectories = do_data_setup_nonlin_without_covariance()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111111(trajectories)
    return spliced_trajectories


def do_data_setup_nonlin_spliced_111000_without_covariance():
    trajectories = do_data_setup_nonlin_without_covariance()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111000(trajectories)
    return spliced_trajectories



def do_data_setup_nonlin_in_params(covariance_trace):
    return do_abstract_data_setup(do_model_setup_nonlin_in_params, do_base_problem_setup, covariance_trace)


def do_data_setup_nonlin_in_params_without_covariance():
    return do_data_setup_nonlin_in_params(numpy.array([1.0, 1.0]))


def do_data_setup_nonlin_in_params_spliced_111111_without_covariance():
    trajectories = do_data_setup_nonlin_in_params_without_covariance()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111111(trajectories)
    return spliced_trajectories

# -----------------------------------------------------------------------------

def do_algorithm_setup(instrumentation_data):
    """
    instrumentation_data None or dictionary with "logger" 
    """
    initial_guesses = numpy.array([1.0, 2.0])

    algorithm_data = dict(solvers.solver_data.algorithm_structure)
    if instrumentation_data is not None:
        algorithm_data["callback"] = instrumentation_data["logger"].log_decision_variables
    algorithm_data["initial_guesses"] = initial_guesses
    algorithm_data["method"] = "CG"
    algorithm_data["tolerance"] = 1E-8
    return algorithm_data

    
def do_instrumentation_setup():
    instrumentation_data = dict(setups.setup_data.instrumentation_data)
    instrumentation_data["logger"] = sosout.DecisionVariableLogger()
    return instrumentation_data


def do_protocol_setup():
    protocol_data = dict(wpd.protocol_data)
    protocol_data["performance_measure"] = mod.sum_squared_residuals_st
    return protocol_data
