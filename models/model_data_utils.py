
import copy
import numpy

import common.utilities
import models.model_data as momoda


# TODO: problem model verificator and synchroniser


def apply_values_to_parameters(values, model_data, problem_data):
    """
    Set model's and problem's parameters to the values given
    values:       list
    model_data:   models.model_data.model_structure
    problem_data: models.model_data.problem.problem_structure
    """
    if problem_data is not None:
        problem_data["parameters"] = copy.deepcopy(values)
    
    if model_data is not None:
        assert(problem_data is not None)
        for ii in range(len(problem_data["parameter_indices"])):
            model_data["parameters"][problem_data["parameter_indices"][ii]] = \
                copy.deepcopy(values[ii])


'''
Set model's and problem's parameters to the values given by the decision variables
opt_sol:      models.model_data.optimisation_problem_point
model_data:   models.model_data.model_structure
problem_data: models.model_data.problem.problem_structure
'''
def apply_decision_variables_to_parameters(opt_sol, model_data, problem_data):
    apply_values_to_parameters(opt_sol["decision_variables"], model_data, problem_data)

'''
return: int
'''
def get_number_of_time_points(problem_data):
    no_timepoints = len(problem_data["time"])
    if problem_data["initial"] == "exclude":
        no_timepoints -= 1
    return no_timepoints


'''
return: int
'''
def get_number_of_decision_variables(problem_data):
    return len(problem_data["parameter_indices"])


'''
return: numpy.ndarray
    the sensitivity trajectories corresponding to the appropriate outputs and parameters
'''
def get_sensitivity_trajectories(dim_states, problem_instance, state_and_sens_trajectories):
    dim_dv = len(problem_instance["parameter_indices"])
    assert(dim_dv > 0)
    assert(dim_dv == len(problem_instance["parameters"]))
    
    trajectories = []
    for ii in range(len(problem_instance["output_indices"])):
        for jj in range(dim_dv):
            index = dim_states+dim_dv*problem_instance["output_indices"][ii]+jj
            trajectory = state_and_sens_trajectories[index]
            trajectories.append(trajectory)
    return numpy.asarray(trajectories)


def get_observable_trajectories(problem_instance, state_trajectories):
    trajectories = []
    for ii in range(len(problem_instance["output_indices"])):
        index = problem_instance["output_indices"][ii]
        trajectories.append(state_trajectories[index])
    return numpy.asarray(trajectories)


def get_observable_calibration_and_validation_trajectories(calib_valid_trajectories, problem_instance):
    '''
    Produces a subset of trajectories on the basis of the output subset
    Raises exception if there are no "output indices"
    calib_valid_trajectories    calib_valid_experimental_dataset
    return                      calib_valid_experimental_dataset
    '''
    if len(problem_instance["output_indices"]) == 0:
        assert(False)
        raise
    
    observables = dict(momoda.calib_valid_experimental_dataset)
    observables["id"] = calib_valid_trajectories["id"]
    observables["calib"]["time"] = calib_valid_trajectories["calib"]["time"]
    observables["valid"]["time"] = calib_valid_trajectories["valid"]["time"]
    calib_observables = []
    valid_observables = []
    for ii in range(len(problem_instance["output_indices"])):
        index = problem_instance["output_indices"][ii]
        calib_observables.append(calib_valid_trajectories["calib"]["observables"][index])
        valid_observables.append(calib_valid_trajectories["valid"]["observables"][index])
    observables["calib"]["observables"] = numpy.asarray(calib_observables)
    observables["valid"]["observables"] = numpy.asarray(valid_observables)
    return observables


def check_correctness_of_measurements_covariance_matrix(prob_inst):
    """
    prob_inst models.model_data.problem_structure
    """
    shape = prob_inst["measurements_covariance_trace"].shape
    assert(len(shape) == 1)
    dim_obs = len(prob_inst["output_indices"])
    assert(dim_obs == shape[0])


def check_no_measurements_covariance_matrix(prob_inst):
    """
    prob_inst models.model_data.problem_structure
    """
    assert(prob_inst["measurements_covariance_trace"] is None)


def calculate_number_of_observations(measurements):
    return common.utilities.size_it(measurements)


def calculate_numberof_degrees_of_freedom(measurements, parameters_to_be_estimated):
    n = calculate_number_of_observations(measurements)
    k = len(parameters_to_be_estimated)
    return n - k


def get_measurement_template_for_all_experiments(problem):
    if len(problem["experiments"]) == 0:
        return numpy.zeros(common.utilities.size_it(problem["outputs"]))
    else:
        meas_count = 0
        for ee in range(len(problem["experiments"])):
            meas_count += common.utilities.size_it(problem["experiments"][ee]["output_measurements"])
        return numpy.zeros(meas_count)