
import numpy

import models.model_data as mmd


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    dx_dt = numpy.multiply(p, u)
    return dx_dt


mock_initial_conditions = [0.0, 1.0]
mock_parameters = [1.0, 0.5]
mock_parameter_indices = [0, 1]
mock_inputs = [1.0, 2.0]


def do_problem_setup():
    problem_instance = dict(mmd.problem_structure)
    problem_instance["initial_conditions"] = mock_initial_conditions
    problem_instance["parameters"] = mock_parameters
    problem_instance["parameter_indices"] = mock_parameter_indices
    problem_instance["inputs"] = mock_inputs
    return problem_instance

    
def do_model_setup():
    model_instance = dict(mmd.model_structure)
    model_instance["parameters"] = mock_parameters
    model_instance["inputs"] = mock_inputs
    model_instance["states"] = mock_initial_conditions
    model_instance["time"] = 0.0
    model_instance["model"] = linear_2p2s_mock
    return model_instance


# returns 10 points from [0.0:1.0], inclusive of initial point
def do_setup_include_initial():
    model_instance = do_model_setup()
    problem_instance = do_problem_setup()
    problem_instance["time"] = numpy.linspace(0.0, 1.0, 10, endpoint=True)
    return model_instance, problem_instance
