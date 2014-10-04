
import unittest
import models.kremlingetal_bioreactor as mk

import copy
import numpy

import common.utilities as cu
import models.model_data
#import results.plot as rps
import results.plot_tiles as rpt
import solvers.initial_value


class TestExperiment04(unittest.TestCase):


    def setup(self):
        return "modelB"


    def do_get_published_data(self):
        # TODO: handle gracefully
        published_data = open("C:/documents/resproj/bench/data.txt", 'r')
        data = numpy.loadtxt(published_data)
        trajectories_without_V = cu.sliceit_astrajectory(data)
        trajectories = numpy.insert( \
            trajectories_without_V, 1, numpy.ones(trajectories_without_V[0].shape), 0)
        return trajectories[0], trajectories[1:]
        

    def test_WIP(self):
        model = self.setup()
        
        t = numpy.linspace(0.0, 20.0, 100)
        p = numpy.ones(len(mk.pmap))
        for par in mk.pmap.items():
            p[par[1]] = mk.pvec[par[0]]
        u = numpy.ones(len(mk.umap))
        for inp in mk.umap.items():
            u[inp[1]] = mk.uvec_0h[inp[0]]
        x = numpy.ones(len(mk.xmap))
        labels = [""] * len(x)
        for ste in mk.xmap.items():
            x[ste[1]] = mk.xvec[ste[0]]
            labels[ste[1]] = ste[0]

        model_data = dict(models.model_data.model_structure)
        model_data["parameters"] = copy.deepcopy(p)
        model_data["inputs"] = copy.deepcopy(u)
        model_data["states"] = copy.deepcopy(x)
        
        problem_data = dict(models.model_data.problem_structure)
        problem_data["initial_conditions"] = copy.deepcopy(x)
        problem_data["time"] = t
        problem_data["parameters"] = copy.deepcopy(p)
        problem_data["inputs"] = copy.deepcopy(u)

        model_func = None
        if model is "modelA":
            model_func = mk.evaluate_modelA
        else:
            model_func = mk.evaluate_modelB
        trajectories = solvers.initial_value.compute_timecourse_trajectories( \
            model_func, model_data, problem_data)
        time, observations = self.do_get_published_data()
        
        rpt.plot_fit(time, observations, t, trajectories, labels, model)


if __name__ == "__main__":
    unittest.main()
