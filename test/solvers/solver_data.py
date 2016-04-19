
import unittest
import solvers.solver_data

class TestSolverData(unittest.TestCase):


    def test_no_keys(self):
        settings = dict(solvers.solver_data.solver_settings)
        user_settings = solvers.solver_data.prune_solver_settings(settings)
        self.assertTrue(len(user_settings) == 0)


    def test_one_key(self):
        settings = dict(solvers.solver_data.solver_settings)
        settings["disp"] = True
        user_settings = solvers.solver_data.prune_solver_settings(settings)
        self.assertTrue(len(user_settings) == 1)


    def test_two_keys(self):
        settings = dict(solvers.solver_data.solver_settings)
        settings["disp"] = True
        settings["eps"] = 1E-3 
        user_settings = solvers.solver_data.prune_solver_settings(settings)
        self.assertTrue(len(user_settings) == 2)


if __name__ == "__main__":
    unittest.main()
