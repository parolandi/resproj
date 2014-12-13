
import copy
import numpy


# TODO: problem model verificator and synchroniser


'''
Set model's and problem's parameters to the values given
values:       list
model_data:   models.model_data.model_structure
problem_data: models.model_data.problem.problem_structure
'''
def apply_values_to_parameters(values, model_data, problem_data):
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
