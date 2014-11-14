
model_structure = {
    "model": None,
    "parameters": [],
    "inputs": [],
    "states": [],
    "outputs": [],
    "time": 0.0,
    }


'''
Defines the approach used for initial conditions
estimate: this initial condition will be estimated and its contribution calculated; a decision variable must exist
exclude: the point will be the exact initial condition; its contribution will not be computed 
include: the point will be the exact initial condition; its contribution will be computed
'''
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
    # TODO observables
    "bounds": None,
    # TODO: establish dedicated "problem_formulation"
    "initial": ("estimate", "exclude", "include"),
    }


# TODO: problem model verificator and synchroniser

'''
Agnostic experimental data set
time:        list
    single time points applicable to all observables
observables: list
    the set of observables, each of which contains a list of measurement points
'''
experimental_dataset = {
    "time": [],
    # measurements subject to noise
    "observables": [],
    }


'''
An experimental data set split into calibration and validations subsets
calib: models.model_data.experimental_dataset
    calibration subset
valid: models.model_data.experimental_dataset
    validation subset
'''
calib_valid_experimental_dataset = {
    "id": "",
    "calib": dict(experimental_dataset),
    "valid": dict(experimental_dataset),
    }


optimisation_problem_point = {
    "decision_variables": [],
    "objective_function": 0.0,
    }
