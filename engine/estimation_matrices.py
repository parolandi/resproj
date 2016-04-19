
import numpy


#sensitivity_trajectories: [df1/dpT, df2/dpT, ..., dfn/dpT]T (n*p x t)
'''
Transform the list of sensitivity trajectories into a matrix of sensitivities
return    numpy.matrix
'''
def prepare_sensitivity_matrix(no_states, no_params, no_timepoints, sensitivity_trajectories):
    # TODO: general case with/without initial point
    #assert(no_timepoints == len(sensitivity_trajectories[0]))
    
    matrix = []
    for param in range(no_params):
        param_sens_mask = [ii for ii in range(param, no_params*no_states, no_params)]
        param_sens =  numpy.ndarray.flatten(sensitivity_trajectories[param_sens_mask])
        matrix.append(param_sens)
    sensitivity_matrix = numpy.transpose(numpy.asmatrix(matrix))
    return sensitivity_matrix


def compute_information_matrix(no_states, no_params, no_timepoints, sensitivity_trajectories):
    sensitivity_matrix = prepare_sensitivity_matrix(no_states, no_params, no_timepoints, sensitivity_trajectories)
    information_matrix = sensitivity_matrix.transpose().dot(sensitivity_matrix)
    return information_matrix
    
    
# TODO: change method name
def calculate_information_matrix(sensitivity_matrix):
    information_matrix = sensitivity_matrix.transpose().dot(sensitivity_matrix)
    return information_matrix


# TODO: deal with singular case
def compute_covariance_matrix(dim_states, no_params, no_timepoints, sensitivity_trajectories):
    information_matrix = compute_information_matrix(dim_states, no_params, no_timepoints, sensitivity_trajectories)
    try:
        covariance_matrix = numpy.linalg.inv(information_matrix)
    except:
        print(information_matrix)
        raise
    return covariance_matrix

    
def calculate_covariance_matrix(sensitivity_matrix):
    information_matrix = sensitivity_matrix.transpose().dot(sensitivity_matrix)
    covariance_matrix = numpy.linalg.inv(information_matrix)
    return covariance_matrix


def calculate_determinant(matrix):
    return numpy.linalg.det(matrix)


def calculate_correlation_matrix(covariance_matrix):
    """
    covariance matrix: numpy.matrix
    returns: numpy.matrix
        correlation matrix
    """
    dims = covariance_matrix.shape
    assert(dims[0] == dims[1])
    # TODO: preconditions
    # assert it is not singular
    
    correlation_matrix = numpy.asmatrix(numpy.zeros([dims[0],dims[1]]))
    for ii in range(dims[0]):
        for jj in range(dims[1]):
            correlation_matrix[ii,jj] = covariance_matrix[ii,jj] / \
                numpy.sqrt(covariance_matrix[ii,ii] * covariance_matrix[jj,jj])
    return correlation_matrix


# TODO: another calculation of the covariance matrix already exists