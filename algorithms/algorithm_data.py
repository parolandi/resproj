
# WIP: 2015-07-29; what is the difference between numerics, method and call?
settings_data = {
    "numerics": None,
    "method": "",
    "call": None,
    "initial_guesses": [],
    "callback": None,
    "tolerance": None,
}

numerics_data_nonrecursive = {
    "least_squares": dict(settings_data),
    "initial_value": dict(settings_data),
    }

# TODO 2015-07-31; change to reporting.enable_trajectories
settings_and_numeric_data = {
    "method": None,
    "integrator": dict(numerics_data_nonrecursive),
    "decision_variable_ranges": [()], # tuples
    "number_of_trials": 0,
    "number_of_trials_to_skip": 0,
    "random_number_generator_seed": 117,
    "enable_trajectories": False,
    }

region_estimation_data = {
    "nonlinear_programming": dict(settings_data),
    "monte_carlo_simulation": dict(settings_and_numeric_data),
    }

numerics_data = {
    "least_squares": dict(settings_data),
    "region_estimation": dict(region_estimation_data),
    "initial_value": dict(settings_data),
    }

'''
montecarlo_multiple_simulation_params = {
    "class": None,
    "decision_variable_ranges": [()], # tuples
    "number_of_trials": 0,
    "random_number_generator_seed": 117,
    "subsolver_params": dict(ss.algorithm_structure),
    "enable_trajectories": False
    }
'''

solvers_data = {
    "model_calibration": None,
    "parameter_confidence_estimation": None,
    }

algorithmic_data = {
    "solvers": None,
    }