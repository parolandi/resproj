
import unittest
import solvers.monte_carlo_multiple_least_squares as smls

import numpy
import models.model_data as mmd
import solvers.initial_value as siv
import models.ordinary_differential as mod
import data.generator as dg


def linear_2p2s_mock(x, t, p, u):
    assert(len(x) == 2)
    assert(len(p) == 2)
    assert(len(u) == 2)
    
    dx_dt = p * u - x
    return dx_dt


class TestMonteCarloMultipleLeastSquares(unittest.TestCase):


    def do_setup(self):
        final_time = 3.0
        intervals = 30
        stdev = 0.2
        
        times = numpy.arange(0.0, final_time, final_time / intervals)
        
        model_instance = dict(mmd.model_structure)
        model_instance["model"] = linear_2p2s_mock
        model_instance["parameters"] = numpy.array([1.0, 2.0])
        model_instance["inputs"] = numpy.array([1.0, 2.0])
        model_instance["states"] = numpy.array([10.0, 8.0])
        model_instance["time"] = 0.0
        
        problem_instance = dict(mmd.problem_structure)
        problem_instance["initial_conditions"] = numpy.array([10.0, 8.0])
        problem_instance["time"] = times
        problem_instance["parameters"] = numpy.array([1.0, 2.0])
        problem_instance["parameter_indices"] = numpy.array([0, 1])
        problem_instance["inputs"] = numpy.array([1.0, 2.0])

        true_measurement_trajectories = numpy.asarray(siv.compute_timecourse_trajectories( \
            mod.linear_2p2s, model_instance, problem_instance))
        
        measurement_noise = numpy.zeros([2, intervals])
        dg.set_seed(117)
        measurement_noise[0] = stdev * dg.normal_distribution(intervals)
        measurement_noise[1] = stdev * dg.normal_distribution(intervals)
        dg.unset_seed()
        
        experimental_measurement_trajectories = true_measurement_trajectories + measurement_noise
        
        problem_instance["outputs"] = experimental_measurement_trajectories
        problem_instance["output_indices"] = [0, 1]

        return model_instance, problem_instance
        

    def test_10trials_meth_NelderMead(self):
        model, problem = self.do_setup()
        algorithm = dict(smls.montecarlo_multiple_optimisation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(-1E3, 1E3), (-1E3, 1E3)]
        algorithm["subsolver_params"]["method"] = "Nelder-Mead" 
        result = smls.montecarlo_multiple_least_squares(model, problem, algorithm)
        actual = result["decision_variables"]
        expected = [[ 1.05282639,  2.05005982], \
                    [ 1.05282858,  2.05003897], \
                    [ 1.05275895,  2.05005285], \
                    [ 1.05283696,  2.0500369 ], \
                    [ 1.05278463,  2.05003175], \
                    [ 1.05279766,  2.05000584], \
                    [ 1.05274985,  2.05000487], \
                    [ 1.05281754,  2.0500136 ], \
                    [ 1.05283625,  2.05002302], \
                    [ 1.05279885,  2.05000861]]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual[0], expected[0])]


if __name__ == "__main__":
    unittest.main()
