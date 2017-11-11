
import unittest
import solvers.monte_carlo_multiple_initial_value as testme
import test.mock.mock as temomo

import numpy
import solvers.initial_value as siv
import data.generator as dg
import results.plot_tiles as rpt


class TestMonteCarloMultipleInitiaValue(unittest.TestCase):


    def do_setup(self):
        final_time = 3.0
        intervals = 30
        stdev = 0.2
        
        times = numpy.arange(0.0, final_time, final_time / intervals)
        model_instance, problem_instance = temomo.do_setup(times)

        trajs = siv.compute_timecourse_trajectories( \
            None, model_instance, problem_instance)
        true_measurement_trajectories, _ = numpy.asarray(trajs)
        
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
        algorithm = dict(testme.montecarlo_multiple_simulation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(-1E3, 1E3), (-1E3, 1E3)]
        #algorithm["subsolver_params"]["method"] = "Nelder-Mead" 
        result = testme.solve(model, problem, algorithm)
        actual = result["succeeded"]["decision_variables"]
        expected = [[ -97.17774704, 351.69932235], \
                    [ -401.33377851, 932.92313607], \
                    [ -538.07660677, 636.12944746], \
                    [ 770.60680152, 797.24921185], \
                    [ -627.1128209, 488.34367688], \
                    [ 863.13342462, 453.69093021], \
                    [ -909.19557985, -698.2144546], \
                    [ 519.41088897, 462.74064042], \
                    [ -824.3850921, -436.49292389], \
                    [ -718.50336146, 167.48817323]]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual[0], expected[0])]
        self.assertEqual(len(result["succeeded"]["objective_function"]), 10)
        self.assertEqual(len(result["failed"]["objective_function"]), 0)
        actual = result["succeeded"]["objective_function"]
        expected = [7798389.5505145723, \
                    56493001.345232479, \
                    29590362.296406806, \
                    48606309.122180611, \
                    20895147.155216932, \
                    24285108.270967092, \
                    43231381.718003511, \
                    17429376.115837783, \
                    22466219.766100377, \
                    9767733.3634064961]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]
        testme.print_montecarlo_multiple_initial_value(0, result)

        if False:
            plot_config = {}
            plot_config["output_names"] = "xyz"
            rpt.plot_ensemble_trajectories(problem["time"], result["succeeded"]["trajectories"], None, None, plot_config)
            rpt.show_all()
        

    # TODO: move from check to actual test
    def test_print(self):
        wall_time = 1
        result = dict(testme.montecarlo_multiple_simulation_result)
        success = dict(testme.solution_ensembles)
        failure = dict(testme.solution_ensembles)
        success["decision_variables"] = numpy.array([[0.1, 0.2], [0.11, 0.21]])
        success["objective_function"] = numpy.array([9, 9.02])
        failure["decision_variables"] = numpy.array([[0.11, 0.21]])
        failure["objective_function"] = numpy.array([9.02])
        result["succeeded"] = success
        result["failed"] = failure
        testme.print_montecarlo_multiple_initial_value(wall_time, result)


if __name__ == "__main__":
    unittest.main()
