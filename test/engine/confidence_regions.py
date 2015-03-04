
import unittest
import engine.confidence_regions as testme

import copy
import numpy

import results.plot as repl
import setups.ordinary_differential as sod
import setups.setup_data as seseda
import solvers.local_sensitivities as solose
import solvers.monte_carlo_multiple_initial_value as mcmiv
import solvers.solver_data as ssd


class TestConfidenceRegions(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestConfidenceRegions, self).__init__(*args, **kwargs)
        self.do_plotting = False

    
    def do_experiment_setup_lin(self):
        config = copy.deepcopy(seseda.experiment_setup)
        config["algorithm_setup"] = self.do_algorithm_setup
        config["data_setup"] = sod.do_baseline_data_setup_spliced_111111_without_covariance
        config["model_setup"] = sod.do_model_setup
        config["problem_setup"] = sod.do_problem_setup_without_covariance
        config["protocol_setup"] = None
        config["protocol_step"]["calib"] = "do"
        config["protocol_step"]["valid"] = "do"
        config["sensitivity_setup"] = solose.compute_timecourse_trajectories_and_sensitivities
        return config

    
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


    def test_compute_nonlinear_confidence_hyperrectangle_lin(self):
        model, problem, algorithm = self.do_setup_lin()
        actual = numpy.asarray(testme.compute_nonlinear_confidence_hyperrectangle(model, problem, algorithm))
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

        if self.do_plotting:
            points = numpy.asarray(actual["decision_variables"])
            repl.plot_scatter(numpy.transpose(points)[0], numpy.transpose(points)[1])


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

        if self.do_plotting:
            points = numpy.asarray(actual["decision_variables"])
            repl.plot_scatter(numpy.transpose(points)[0], numpy.transpose(points)[1])


    def test_compute_linearised_confidence_region_intervals_lin(self):
        config = self.do_experiment_setup_lin()
        best = {}
        best['objective_function'] = 37.641550819151604
        best['decision_variables'] = [ 1.30352132,  2.24589073]
        intervals = numpy.asarray(testme.compute_linearised_confidence_intervals(config, best))
        expected = numpy.asarray([[0.89143076, 1.71561188], [2.03984545, 2.45193601]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(intervals.flatten(), expected.flatten())]
        
        if self.do_plotting:
            repl.plot_box(intervals)


    def test_compute_linearised_confidence_region_ellipsoid_lin(self):
        config = self.do_experiment_setup_lin()
        best = {}
        best['objective_function'] = 37.641550819151604
        best['decision_variables'] = [ 1.30352132,  2.24589073]
        covariance = numpy.asarray(testme.compute_linearised_confidence_region_ellipsoid(config, best))
        expected = numpy.asarray([[1.14621592e-01, 1.45127430e-10], [1.45127430e-10, 2.86553976e-02]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(covariance.flatten(), expected.flatten())]
        
        if self.do_plotting:
            repl.plot_ellipse(best['decision_variables'], covariance)


    # TODO: note that this is calling two methods at the time and thus is not a unit-test
    # but an integration test; leaving here for the moment for convenience
    def test_compute_linearised_confidence_region_ellipsoid_and_intervals_lin(self):
        config = self.do_experiment_setup_lin()
        best = {}
        best['objective_function'] = 37.641550819151604
        best['decision_variables'] = [ 1.30352132,  2.24589073]
        intervals = testme.compute_linearised_confidence_intervals(config, best)
        expected = numpy.asarray([[0.89143075929592142, 1.7156118807040786], [2.0398454509198882, 2.4519360090801121]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(numpy.asarray(intervals).flatten(), expected.flatten())]
        covariance = testme.compute_linearised_confidence_region_ellipsoid(config, best)
        expected = numpy.asarray([[1.14621592e-01, 1.45127430e-10], [1.45127430e-10, 2.86553976e-02]])
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(numpy.asarray(covariance).flatten(), numpy.asarray(expected).flatten())]
        
        if self.do_plotting:
            repl.plot_ellipse_and_box(best['decision_variables'], covariance, intervals)


if __name__ == "__main__":
    unittest.main()
