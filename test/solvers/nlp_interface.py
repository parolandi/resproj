
import unittest
import solvers.nlp_interface as testme
import test.mock.mock as testmetoo

import solvers.solver_data as sosoda


class TestNlpInterface(unittest.TestCase):

    
    def do_algorithm_setup_local(self):
        data = dict(sosoda.algorithm_structure)
        data["class"] = testme.solesq.solve
        data["method"] = "Nelder-Mead"
        data["initial_guesses"] = [1.0, 1.0]
        return data
        
        
    def do_algorithm_setup_global(self):
        data = dict(testme.somcmlesq.montecarlo_multiple_optimisation_params)
        data["class"] = testme.somcmlesq.solve
        data["number_of_trials"] = 10
        data["decision_variable_ranges"] = [(0, 100), (0, 100)]
        # sosoda.algorithm_structure
        data["subsolver_params"]["method"] = "Nelder-Mead" 
        return data


    def test_nlp_interface(self):
        experiment = testmetoo.do_experiment_with_protocol_as_invariant()
        model, _, problem = testmetoo.get_model_data_problem(experiment)
        local = self.do_algorithm_setup_local()
        actual = testme.solve(model, problem, local)
        [self.assertAlmostEquals(act, exp, 8) for act, exp in zip(actual.x, [1.0, 1.0])]
        mcm = self.do_algorithm_setup_global()
        actuals = testme.solve(model, problem, mcm)
        [self.assertAlmostEquals(act, exp, 4) for act, exp in zip(actuals.x, [1.0, 1.0])]


if __name__ == "__main__":
    unittest.main()