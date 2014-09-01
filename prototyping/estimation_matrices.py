
import numpy


def prepare_sensitivity_matrix(no_params, no_timepoints, sensitivity_trajectories):
    flat = sensitivity_trajectories.flatten()
    no_meas = no_timepoints * no_params
    sensitivity_matrix = numpy.asmatrix(flat.reshape((no_params, no_meas)).transpose())
    return sensitivity_matrix
    

def compute_information_matrix(no_params, no_timepoints, sensitivity_trajectories):
    sensitivity_matrix = prepare_sensitivity_matrix(no_params, no_timepoints, sensitivity_trajectories)
    information_matrix = sensitivity_matrix.transpose().dot(sensitivity_matrix)
    return information_matrix
    
    
# TODO: change method name
def calculate_information_matrix(sensitivity_matrix):
    information_matrix = sensitivity_matrix.transpose().dot(sensitivity_matrix)
    return information_matrix


# TODO: deal with singular case
def compute_covariance_matrix(no_params, no_timepoints, sensitivity_trajectories):
    information_matrix = compute_information_matrix(no_params, no_timepoints, sensitivity_trajectories)
    covariance_matrix = numpy.linalg.inv(information_matrix)
    return covariance_matrix

    
def calculate_covariance_matrix(sensitivity_matrix):
    information_matrix = sensitivity_matrix.transpose().dot(sensitivity_matrix)
    covariance_matrix = numpy.linalg.inv(information_matrix)
    return covariance_matrix


# TODO: add proper unit tests
    