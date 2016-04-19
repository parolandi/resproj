
import unittest
import solvers.dynamic_optimisation as testme

import copy
import numpy

import setups.ordinary_differential as sod
import solvers.solver_data as ssd


# TODO: test callback
class TestDynamicOptimisation(unittest.TestCase):


    def do_setup(self):
        model = sod.do_model_setup()
        data = sod.do_baseline_data_setup_spliced_111111_without_covariance()
        problem = sod.do_problem_setup_without_covariance(model, data["calib"])
        
        # needs to be sufficiency large otherwise will be chasing ghosts
        problem["confidence_region"]["ssr"] = 43
 
        algorithm = self.do_algorithm_setup()
        return model, problem, algorithm


    def do_algorithm_setup(self):
        algorithm = copy.deepcopy(ssd.algorithm_structure)
        algorithm["initial_guesses"] = numpy.asarray([1.0])
        algorithm["method"] = 'SLSQP'
        return algorithm
        

    def do_performance_measure_w_args(self, x, x0):
        return x0 - x
        
    
    def do_performance_measure_wo_args(self, x):
        return (-1) * x

    
    def do_constraint(self, x, x0):
        return x0 - x


    def do_form_constraint(self, x0):
        constraint_list = []
        constraint_list.append( \
                      {'type': 'ineq', \
                       'fun': self.do_constraint, \
                       'args': (x0,)})
        constraints = tuple(constraint_list)
        return constraints

    
    # TODO: legacy-ish
    def regression_test_solve(self):
        model, problem, algorithm = self.do_setup()
        problem["confidence_region"]["parameter_index"] = 0

        problem["performance_measure"] = testme.maximise_it
        upper = testme.solve(model, problem, algorithm)
        problem["performance_measure"] = testme.minimise_it
        lower = testme.solve(model, problem, algorithm)

        self.assertEquals(upper.status+lower.status, 0)
        self.assertAlmostEquals(upper.x, 1.59365765, 8)
        self.assertAlmostEquals(lower.x, 1.01338741, 8)

        problem["confidence_region"]["parameter_index"] = 1

        problem["performance_measure"] = testme.maximise_it
        upper = testme.solve(model, problem, algorithm)
        problem["performance_measure"] = testme.minimise_it
        lower = testme.solve(model, problem, algorithm)

        self.assertEquals(upper.status+lower.status, 0)
        self.assertAlmostEquals(upper.x, 2.49178146, 8)
        self.assertAlmostEquals(lower.x, 2.00000001, 8)


    def test_solve_std_perf_meas_wo_args(self):
        model, problem, algorithm = self.do_setup()
        
        problem["performance_measure"] = self.do_performance_measure_wo_args
        bounds = [tuple([0,10])]
        problem["bounds"] = tuple(bounds)
        actual = testme.solve_std(model, problem, algorithm)
        expected = -10
        self.assertAlmostEqual(actual.fun, expected, 12)
        

    def test_solve_std_perf_meas_w_args(self):
        model, problem, algorithm = self.do_setup()
        
        problem["performance_measure"] = self.do_performance_measure_w_args
        problem["performance_measure_args"] = tuple([1])
        bounds = [tuple([0,10])]
        problem["bounds"] = tuple(bounds)
        actual = testme.solve_std(model, problem, algorithm)
        expected = -9
        self.assertAlmostEqual(actual.fun, expected, 12)


    def test_solve_std_perf_meas_wo_args_w_constraints(self):
        model, problem, algorithm = self.do_setup()
        
        problem["performance_measure"] = self.do_performance_measure_wo_args
        problem["constraints"] = self.do_form_constraint(5)
        bounds = [tuple([0,10])]
        problem["bounds"] = tuple(bounds)
        actual = testme.solve_std(model, problem, algorithm)
        expected = -5
        self.assertAlmostEqual(actual.fun, expected, 12)


    def test_solve_std_perf_meas_w_args_w_constraints(self):
        model, problem, algorithm = self.do_setup()
        
        problem["performance_measure"] = self.do_performance_measure_w_args
        problem["performance_measure_args"] = tuple([1])
        problem["constraints"] = self.do_form_constraint(5)
        bounds = [tuple([0,10])]
        problem["bounds"] = tuple(bounds)
        actual = testme.solve_std(model, problem, algorithm)
        expected = -4
        self.assertAlmostEqual(actual.fun, expected, 12)


if __name__ == "__main__":
    unittest.main()