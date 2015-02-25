
import unittest
import engine.confidence_regions as testme

import copy
import numpy

import setups.ordinary_differential as sod
import solvers.monte_carlo_multiple_initial_value as mcmiv
import solvers.solver_data as ssd

import matplotlib.pyplot as pp


class TestConfidenceRegions(unittest.TestCase):


    def do_setup_lin(self):
        algorithm = self.do_algorithm_setup()
        data = sod.do_baseline_data_setup_spliced_111111_without_covariance()
        model = sod.do_model_setup_lin()
        problem = sod.do_problem_setup_without_covariance(model, data["calib"])
        problem["nonlinear_confidence_region"]["ssr"] = 43
        return model, problem, algorithm


    def do_setup_nonlin(self):
        algorithm = self.do_algorithm_setup()
        data = sod.do_data_setup_nonlin_spliced_111111_without_covariance()
        model = sod.do_model_setup_nonlin()
        problem = sod.do_problem_setup_without_covariance(model, data["calib"])
        problem["nonlinear_confidence_region"]["ssr"] = 43
        return model, problem, algorithm

    
    def do_algorithm_setup(self):
        algorithm = copy.deepcopy(ssd.algorithm_structure)
        algorithm["initial_guesses"] = numpy.asarray([1.0])
        algorithm["method"] = 'SLSQP'
        return algorithm
        

    def test_compute_nonlinear_confidence_interval_lin(self):
        model, problem, algorithm = self.do_setup_lin()
        actual = testme.compute_nonlinear_confidence_interval(model, problem, algorithm, 0)
        expected = [1.01338741, 1.59365765]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]


    def test_compute_nonlinear_confidence_intervals_lin(self):
        model, problem, algorithm = self.do_setup_lin()
        actual = numpy.asarray(testme.compute_nonlinear_confidence_intervals(model, problem, algorithm))
        _ = numpy.asarray([[1.01338741, 1.59365765], [2.00000001, 2.49178146]])
        expected = numpy.asarray([[1.01338741, 1.59365765], [2.0040739383273261, 2.4877075291690458]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual.flatten(), expected.flatten())]


    def test_empihbnci_lin(self):
        model, problem, _ = self.do_setup_lin()
        algorithm = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(1.01338741, 1.59365765), (2.00000001, 2.49178146)]
        result = testme.evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals( \
            model, problem, algorithm)
        actual = result["objective_function"]
        expected = [ 38.14628465, 41.32395438, 39.65061399, 40.98962304, 39.13358795,  39.49045378, 40.72301099, 38.8659546,  39.339134,   38.4672953 ]
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual, expected)]
        # TODO should also test decision variables

    
    def test_filter_nonlinear_confidence_region_points_lin(self):
        model, problem, _ = self.do_setup_lin()
        algorithm = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm["number_of_trials"] = 10
        algorithm["decision_variable_ranges"] = [(1.01338741, 1.59365765), (2.00000001, 2.49178146)]
        prelim = testme.evaluate_multiple_points_in_hyperrectangle_by_nonlinear_confidence_intervals( \
            model, problem, algorithm)
        cutoff = 38.47
        result = testme.filter_nonlinear_confidence_region_points(prelim, cutoff)
        self.assertTrue(len(result["objective_function"]) == 2)
        # TODO should also test individual values


    def test_compute_nonlinear_confidence_region_points_lin(self):
        best_point = {}
        best_point["decision_variables"] = [ 1.30352132,  2.24589073]
        best_point["objective_function"] = 37.641550819151604
        
        model, problem, algorithm_rf = self.do_setup_lin()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        actual = testme.compute_nonlinear_confidence_region_points( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        self.assertEquals(len(actual["objective_function"]), 7834)

        if False:
            points = numpy.asarray(actual["decision_variables"])
            pp.plot(numpy.transpose(points)[0], numpy.transpose(points)[1], 'o')
            pp.show()


    def test_compute_nonlinear_confidence_region_points_nonlin(self):
        best_point = {}
        best_point["decision_variables"] = [ 1.2175145 ,  2.15319774]
        best_point["objective_function"] = 37.67831358169179
        
        model, problem, algorithm_rf = self.do_setup_nonlin()
        algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
        algorithm_mc["number_of_trials"] = 10000
        actual = testme.compute_nonlinear_confidence_region_points( \
            model, problem, algorithm_rf, algorithm_mc, best_point)
        self.assertEquals(len(actual["objective_function"]), 7841)

        if False:
            points = numpy.asarray(actual["decision_variables"])
            pp.plot(numpy.transpose(points)[0], numpy.transpose(points)[1], 'o')
            pp.show()


if __name__ == "__main__":
    unittest.main()
    