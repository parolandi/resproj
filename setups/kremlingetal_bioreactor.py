
import copy
import numpy

import common.utilities as cu
import metrics.ordinary_differential as mod
import models.kremlingetal_bioreactor as mkb
import models.model_data


def do_model_setup(model_key):
    p = numpy.ones(len(mkb.pmap))
    for par in mkb.pmap.items():
        p[par[1]] = mkb.pvec[par[0]]
    
    u = numpy.ones(len(mkb.umap))
    for inp in mkb.umap.items():
        u[inp[1]] = mkb.uvec_0h[inp[0]]
    
    x = numpy.ones(len(mkb.xmap))
    
    # WIP
#    labels = [""] * len(x)
    for ste in mkb.xmap.items():
        x[ste[1]] = mkb.xvec[ste[0]]
#        labels[ste[1]] = ste[0]
    
    model_data = dict(models.model_data.model_structure)
    model_data["parameters"] = copy.deepcopy(p)
    model_data["inputs"] = copy.deepcopy(u)
    model_data["states"] = copy.deepcopy(x)
    if model_key is "modelA":
        model_data["model"] = mkb.evaluate_modelA
    else:
        model_data["model"] = mkb.evaluate_modelB
    
    return model_data


def do_model_setup_model_A():
    return do_model_setup("modelA")


def do_model_setup_model_B():
    return do_model_setup("modelB")


def do_get_published_data():
    # TODO: handle gracefully
    published_data = open("C:/documents/resproj/bench/data_time_0_20.txt", 'r')
    data = numpy.loadtxt(published_data)
    trajectories_without_V = cu.sliceit_astrajectory(data)
    return trajectories_without_V[0], trajectories_without_V[1:]


def do_problem_setup(model_data):
    tt = numpy.linspace(0.0, 20.0, 11, endpoint=True)
    
    problem_data = dict(models.model_data.problem_structure)
    problem_data["initial_conditions"] = copy.deepcopy(model_data["states"])
    problem_data["time"] = tt
    problem_data["parameters"] = copy.deepcopy(model_data["parameters"])
    problem_data["inputs"] = copy.deepcopy(model_data["inputs"])

    problem_data["performance_measure"] = mod.sum_squared_residuals_st
    problem_data["parameter_indices"] = [0, 3, 5, 8, 9]
    problem_data["parameters"] = numpy.zeros(len(problem_data["parameter_indices"]))
    problem_data["bounds"] = [(0,None), (0,None), (0,None), (0,None), (0,None)]
    
    _, observations = do_get_published_data()
    problem_data["output_indices"] = [1, 2, 3, 4, 5]
    problem_data["outputs"] = observations

    return problem_data


# TODO: think where this should go
def do_labels():
    labels = [""] * len(mkb.xmap)
    for ste in mkb.xmap.items():
        labels[ste[1]] = ste[0]
    
    return labels
