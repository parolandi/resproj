
import numpy

import data.generator as dg


def do_sampling(algorithm):
    """
    return numpy.array
    """
    dv_count = len(algorithm["decision_variable_ranges"])
    dv_ranges = algorithm["decision_variable_ranges"]
    trials_count = algorithm["number_of_trials"]
    seed = algorithm["random_number_generator_seed"]
    return draw_samples(dv_count, dv_ranges, trials_count, seed)


def draw_samples(dv_count, dv_ranges, trials_count, seed):
    """
    return numpy.array
    """
    monte_carlo_points = []
    dg.set_seed(seed)
    for ii in range(dv_count):
        bounds = dv_ranges[ii]
        points = dg.uniform_distribution(trials_count)
        scaled_points = bounds[0] + points * (bounds[1] - bounds[0]) 
        monte_carlo_points.append(scaled_points)
    dg.unset_seed()
    return numpy.asarray(monte_carlo_points)
