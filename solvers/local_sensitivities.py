
import copy
import numpy

import models.model_data_utils as mmdu
import solvers.initial_value as siv


# TODO: do not work on lists
def compute_timecourse_trajectories_and_sensitivities(model_data, problem_data):
    # TODO: preconditions
    assert(problem_data["parameter_indices"] > 0)
    
    eps = 1E-5
    
    nominal_trajectories = siv.compute_timecourse_trajectories(None, model_data, problem_data)
    nominal_param_vals = copy.deepcopy(problem_data["parameters"])
    dim_param = len(problem_data["parameter_indices"])
    dim_states = len(nominal_trajectories)
    sensitivities = []
    for param in range(dim_param):
        param_val = copy.deepcopy(nominal_param_vals)
        param_val[param] = (1 + eps) * nominal_param_vals[param]
        delta = eps * nominal_param_vals[param]
        if delta == 0.0 or nominal_param_vals[param] < eps:
            param_val[param] = eps
            delta = eps
        mmdu.apply_values_to_parameters(param_val, model_data, problem_data)
        perturbed_trajectories = siv.compute_timecourse_trajectories(None, model_data, problem_data)
        for state in range(len(perturbed_trajectories)):
            sensitivity = []
            for time in range(len(perturbed_trajectories[state])):
                sensitivity.append((perturbed_trajectories[state][time] - nominal_trajectories[state][time]) / delta)
            sensitivities.append(sensitivity)
    '''
    s1p1
    s2p1
    s3p1
    s1p2
    s2p2
    s3p2
    -->
    s1p1
    s1p2
    s2p1
    s2p2
    s3p1
    s3p2
    '''
    sens_state_wise = numpy.zeros([dim_param*dim_states, mmdu.get_number_of_time_points(problem_data)])
    sens_param_wise = numpy.asarray(sensitivities)
    for state in range(dim_states):
        for param in range(dim_param):
            sens_state_wise[dim_param*state+param,] = sens_param_wise[state+dim_states*param,]
    sensitivity_trajectories = numpy.concatenate((nominal_trajectories, sens_state_wise))
    return numpy.asarray(sensitivity_trajectories)
