
import copy
import numpy

import common.utilities as cu
import data.experimental_data_splicing as deds
import experiments.protocol_data as epd
import metrics.ordinary_differential as mod
import models.kremlingetal_bioreactor as mkb
import models.model_data
import setups.setup_data
import solvers.least_squares


def do_model_setup(model_key):
    p = numpy.ones(len(mkb.pmap))
    for par in mkb.pmap.items():
        p[par[1]] = mkb.pvec[par[0]]
    
    u = numpy.ones(len(mkb.umap))
    for inp in mkb.umap.items():
        u[inp[1]] = mkb.uvec_0h[inp[0]]
    
    x = numpy.ones(len(mkb.xmap))
    
    for ste in mkb.xmap.items():
        x[ste[1]] = mkb.xvec[ste[0]]
    
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
    return trajectories_without_V


def do_get_published_data_spliced_111111():
    trajectories_without_V = do_get_published_data()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111111(trajectories_without_V)
    return spliced_trajectories


def do_get_published_data_spliced_111000():
    trajectories_without_V = do_get_published_data()
    spliced_trajectories = deds.splice_raw_data_with_pattern_111000(trajectories_without_V)
    return spliced_trajectories


def do_problem_setup(model_data, data_instance):
    assert(model_data is not None)
    assert(data_instance is not None)
    
    problem_data = dict(models.model_data.problem_structure)
    problem_data["initial_conditions"] = copy.deepcopy(model_data["states"])
    problem_data["time"] = data_instance["time"]
    problem_data["parameters"] = copy.deepcopy(model_data["parameters"])
    problem_data["inputs"] = copy.deepcopy(model_data["inputs"])

    problem_data["performance_measure"] = mod.sum_squared_residuals_st
    problem_data["parameter_indices"] = [0, 3, 5, 8, 9]
    problem_data["parameters"] = numpy.zeros(len(problem_data["parameter_indices"]))
    
    for ii in range(len(problem_data["parameter_indices"])):
        problem_data["parameters"][ii] = copy.deepcopy(model_data["parameters"][problem_data["parameter_indices"][ii]])
    
    problem_data["bounds"] = [(0,None), (0,None), (0,None), (0,None), (0,None)]
    
    problem_data["output_indices"] = [1, 2, 3, 4, 5]
    problem_data["outputs"] = data_instance["observables"]
    assert(len(["output_indices"]) == len(["outputs"]))

    return problem_data


# TODO: think where this should go
def do_labels():
    labels = [""] * len(mkb.xmap)
    for ste in mkb.xmap.items():
        labels[ste[1]] = ste[0]
    
    return labels


def do_algorithm_setup(instrumentation_data):
    p = numpy.ones(len(mkb.pmap))
    for par in mkb.pmap.items():
        p[par[1]] = mkb.pvec[par[0]]
    pi = [0, 3, 5, 8, 9]
    initial_guesses = []
    for ii in range(len(pi)):
        initial_guesses.append(copy.deepcopy(p[pi[ii]]))
    algorithm_data = dict(solvers.solver_data.algorithm_structure)
    if instrumentation_data is not None:
        algorithm_data["callback"] = instrumentation_data["logger"].log_decision_variables
    algorithm_data["initial_guesses"] = initial_guesses
    algorithm_data["method"] = "Nelder-Mead"
    return algorithm_data

    
def do_instrumentation_setup():
    instrumentation_data = dict(setups.setup_data.instrumentation_data)
    instrumentation_data["logger"] = solvers.least_squares.DecisionVariableLogger()
    return instrumentation_data


def do_protocol_setup():
    protocol_data = dict(epd.protocol_data)
    protocol_data["performance_measure"] = mod.sum_squared_residuals_st
    return protocol_data
