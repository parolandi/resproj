
import unittest
import models.kremlingetal_bioreactor as mk

import copy
import numpy

import models.model_data
import solvers.initial_value


class TestKremlingEtAlBioreactor(unittest.TestCase):


    def test_regression(self):
        t = numpy.linspace(0.0, 20.0, 11)
        p = numpy.ones(len(mk.pmap))
        for par in mk.pmap.items():
            p[par[1]] = mk.pvec[par[0]]
        u = numpy.ones(len(mk.umap))
        for inp in mk.umap.items():
            u[inp[1]] = mk.uvec_0h[inp[0]]
        x = numpy.ones(len(mk.xmap))
        for ste in mk.xmap.items():
            x[ste[1]] = mk.xvec[ste[0]]

        model_data = dict(models.model_data.model_structure)
        model_data["parameters"] = copy.deepcopy(p)
        model_data["inputs"] = copy.deepcopy(u)
        model_data["states"] = copy.deepcopy(x)
        problem_data = dict(models.model_data.problem_structure)
        problem_data["initial_conditions"] = copy.deepcopy(x)
        problem_data["time"] = t
        problem_data["parameters"] = copy.deepcopy(p)
        problem_data["inputs"] = copy.deepcopy(u)

        trajectories = solvers.initial_value.compute_timecourse_trajectories( \
            mk.evaluate_modelB, model_data, problem_data)
        
        snapshots = solvers.initial_value.compute_trajectory_st( \
            mk.evaluate_modelB, model_data, problem_data)

        self.assertEqual(len(t), 11)
        
        # trajectory testing
        expected = numpy.asarray([0.1        , 0.45231151, 0.43154884, 0.41647925, 0.40731195, 0.40174070, \
            0.39835725, 0.39630344, 0.39505712, 0.39430094, 0.39384223])
        actual = trajectories[1]
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        
        expected = numpy.asarray([2.         , 0.08479020, 0.06961922, 0.07252712, 0.07442350, 0.07562755, \
            0.07637892, 0.07684270, 0.07712704, 0.07730064, 0.07740635])
        actual = trajectories[2]
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]

        # snapshot testing        
        expected = copy.deepcopy(x)
        actual = snapshots[0]
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        
        expected = numpy.asarray([1., 0.45231151, 0.08479020, 0.29593212, 0.01285288, 0.02710117])
        actual = snapshots[1]
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]

        expected = numpy.asarray([1., 0.39384223, 0.07740635, 0.10892526, 0.01189742, 0.06714264])
        actual = snapshots[len(t)-1]
        [self.assertAlmostEquals(exp, act) for exp, act in zip(expected, actual)]
        
    
    # TODO: test published data
    
    
if __name__ == "__main__":
    unittest.main()
