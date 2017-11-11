
import numpy
# TODO: migrate to scipy
# TODO: rename to noise generator
import numpy.random


def set_seed(value):
    numpy.random.seed(value)

    
def unset_seed():
    numpy.random.seed()


def normal_distribution(count):
    return numpy.random.randn(count)


def uniform_distribution(count):
    return numpy.random.rand(count)


def compute_measurement_errors(problem_data, data_instance):
    """
    Compute experimental errors
        assume normal distribution and 99.7%
        use measurements' covariance matrix
    returns
        errors_calib numpy.array NT*NO
        errors_valid numpy.array NT*NO
    """
    cvm = problem_data["measurements_covariance_trace"]
    calib_data = data_instance["calib"]["time"]
    valid_data = data_instance["valid"]["time"]
    return calculate_measurement_errors(cvm, calib_data, valid_data)


def calculate_measurement_errors(cvm, calib_times, valid_times):
    """
    Compute experimental errors
        assume normal distribution and 99.7%
    returns
        errors_calib numpy.array NT*NO
        errors_valid numpy.array NT*NO
    """    # at 99.7%
    error_factor = 3

    calib_errors = []
    valid_errors = []
    calib_dimT = len(calib_times)
    valid_dimT = len(valid_times)
    for ii in range(len(cvm)):
        calib_errors.append(error_factor * numpy.ones(calib_dimT) * cvm[ii])
        valid_errors.append(error_factor * numpy.ones(valid_dimT) * cvm[ii])
    errors_calib = numpy.asarray(calib_errors)
    errors_valid = numpy.asarray(valid_errors)
    return errors_calib, errors_valid
