
#import numpy

model_structure = {
    "model": None,
    "parameters": [],
    "inputs": [],
    "states": [],
    "outputs": [],
    "time": 0.0,
    }


# defines the approach used for initial conditions
# estimate: this initial condition will be estimated and its contribution calculated; a decision variable must exist
# exclude: the point will be the exact initial condition; its contribution will not be computed 
# include: the point will be the exact initial condition; its contribution will be computed
problem_formulation = {
    "initial_conditions": ("estimate", "exclude", "include")
    }


problem_structure = {
    "initial_conditions": [],
    # TODO: change to "times"
    "time": [],
    "performance_measure": None,
    "parameters": [],
    "parameter_indices": [],
    "inputs": [],
    "outputs": [],
    "output_indices": [],
    "bounds": None,
    # TODO: establish dedicated "problem_formulation"
    "initial": ("estimate", "exclude", "include"),
    }


# TODO: problem model verificator and synchroniser