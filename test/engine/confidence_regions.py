
import unittest
import engine.confidence_regions as testme

import copy
import numpy

import metrics.ordinary_differential as mod
import models.model_data_utils as mmdu
import setups.ordinary_differential as sod
import solvers.least_squares as sls
import solvers.monte_carlo_multiple_initial_value as mcmiv
import solvers.solver_data as ssd

import matplotlib.pyplot as pp


class TestConfidenceRegions(unittest.TestCase):


    def do_setup(self):
        model = sod.do_model_setup()
        data = sod.do_baseline_data_setup_spliced_111111_without_covariance()
        problem = sod.do_problem_setup_without_covariance(model, data["calib"])
        problem["nonlinear_confidence_region"]["ssr"] = 43
        algorithm = self.do_algorithm_setup()
        return model, problem, algorithm


    def do_algorithm_setup(self):
        algorithm = copy.deepcopy(ssd.algorithm_structure)
        algorithm["initial_guesses"] = numpy.asarray([1.0])
        algorithm["method"] = 'SLSQP'
        return algorithm
        

    def test_compute_nonlinear_confidence_interval(self):
        model, problem, algorithm = self.do_setup()
        actual = testme.compute_nonlinear_confidence_interval(model, problem, algorithm, 0)
        expected = [1.01338741, 1.59365765]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]


    def test_compute_nonlinear_confidence_intervals(self):
        model, problem, algorithm = self.do_setup()
        actual = numpy.asarray(testme.compute_nonlinear_confidence_intervals(model, problem, algorithm))
        _ = numpy.asarray([[1.01338741, 1.59365765], [2.00000001, 2.49178146]])
        expected = numpy.asarray([[1.01338741, 1.59365765], [2.0040739383273261, 2.4877075291690458]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual.flatten(), expected.flatten())]


    def test_empihbnci(self):
        model, problem, _ = self.do_setup()
        algorithm = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(1.01338741, 1.59365765), (2.00000001, 2.49178146)]
        result = testme.evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals( \
            model, problem, algorithm)
        actual = result["objective_function"]
        expected = [ 38.14628465, 41.32395438, 39.65061399, 40.98962304, 39.13358795,  39.49045378, 40.72301099, 38.8659546,  39.339134,   38.4672953 ]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]
        # TODO should also test decision variables

    
    def donot_test_filter_nonlinear_confidence_region_points(self):
        model, problem, _ = self.do_setup()
        algorithm = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(1.01338741, 1.59365765), (2.00000001, 2.49178146)]
        prelim = testme.evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals( \
            model, problem, algorithm)
        cutoff = 38.47
        result = testme.filter_nonlinear_confidence_region_points(prelim, cutoff)
        self.assertTrue(len(result["objective_function"]) == 2)
        # TODO should also check individual values


    def test_compute_nonlinear_confidence_region_points(self):
        model, problem, _ = self.do_setup()
        algorithm = dict(ssd.algorithm_structure)
        algorithm["initial_guesses"] = problem["parameters"]
        algorithm["method"] = 'SLSQP'
        dvs = sls.solve(model, problem, algorithm)
        mmdu.apply_values_to_parameters(dvs.x, model, problem)
        obj = mod.sum_squared_residuals_st(None, None, model, problem)
        best_point = {}
        best_point["decision_variables"] = dvs.x
        best_point["objective_function"] = obj
        
        model, problem, algorithm_rf = self.do_setup()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        actual = testme.compute_nonlinear_confidence_region_points( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        points = numpy.asarray(actual["decision_variables"])
        self.assertEquals(len(numpy.transpose(actual["objective_function"])), 7834)

        # plot
        pp.plot(numpy.transpose(points)[0], numpy.transpose(points)[1], 'o')
        pp.show()


if __name__ == "__main__":
    unittest.main()
    