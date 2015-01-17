
import unittest
import solvers.monte_carlo_multiple_least_squares as testme

import numpy
import models.model_data as mmd
import solvers.initial_value as siv
import metrics.ordinary_differential as meod
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
        problem_instance["performance_measure"] = meod.sum_squared_residuals_st

        true_measurement_trajectories = numpy.asarray(siv.compute_timecourse_trajectories( \
            None, model_instance, problem_instance))
        
        measurement_noise = numpy.zeros([2, intervals])
        dg.set_seed(117)
        measurement_noise[0] = stdev * dg.normal_distribution(intervals)
        measurement_noise[1] = stdev * dg.normal_distribution(intervals)
        dg.unset_seed()
        
        experimental_measurement_trajectories = true_measurement_trajectories + measurement_noise
        
        problem_instance["outputs"] = experimental_measurement_trajectories
        problem_instance["output_indices"] = [0, 1]

        return model_instance, problem_instance
        

    def test_solve_10trials_meth_NelderMead(self):
        model, problem = self.do_setup()
        algorithm = dict(testme.montecarlo_multiple_optimisation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(-1E3, 1E3), (-1E3, 1E3)]
        algorithm["subsolver_params"]["method"] = "Nelder-Mead" 
        result = testme.solve_all(model, problem, algorithm)
        
        actual = [result["all"][ii]["decision_variables"] for ii in range(len(result["all"]))]
        expected = [[ 1.05277329,  2.05002794], \
                    [ 1.0527749 ,  2.05003731], \
                    [ 1.05284503,  2.05004795], \
                    [ 1.05277353,  2.05004251], \
                    [ 1.05284875,  2.05002186], \
                    [ 1.05282161,  2.05004994], \
                    [ 1.05275604,  2.05003186], \
                    [ 1.05285143,  2.05003992], \
                    [ 1.05283032,  2.05004985], \
                    [ 1.05278199,  2.05001299]]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual[0], expected[0])]
        actual = [result["local"][ii]["decision_variables"] for ii in range(len(result["local"]))]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual[0], expected[0])]

        actual = [result["all"][ii]["objective_function"] for ii in range(len(result["all"]))]
        expected = [1.6631843480296808, \
                    1.6631843451521644, \
                    1.6631843773319452, \
                    1.6631843501151409, \
                    1.663184379608265, \
                    1.6631843571171214, \
                    1.6631843652319205, \
                    1.6631843768521017, \
                    1.66318436384234, \
                    1.6631843669229727]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]
        actual = [result["local"][ii]["objective_function"] for ii in range(len(result["local"]))]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]
        actual = result["global"]["objective_function"]
        print(actual)
        expected = 1.66318434515
        self.assertAlmostEquals(actual, expected, 8)
        actual = result["global"]["decision_variables"]
        expected = [ 1.0527749, 2.05003731]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]


    # TODO: move from check to actual test
    def test_print(self):
        wall_time = 1
        result = dict(testme.montecarlo_multiple_optimisation_result)
        solpnt1 = dict(testme.solution_point)
        solpnt1["decision_variables"] = numpy.array([0.1, 0.2])
        solpnt2 = dict(testme.solution_point)
        solpnt2["decision_variables"] = numpy.array([0.11, 0.21])
        solpnt2["objective_function"] = 9.01
        result["local"] = [solpnt1, solpnt2]
        result["global"] = solpnt2
        nom_params = [1.0, 2.0]
        nom_ssr = 10
        fit_ssr = 9
        testme.print_montecarlo_multiple_least_squares(wall_time, result, nom_params, nom_ssr, fit_ssr)
        

if __name__ == "__main__":
    unittest.main()
