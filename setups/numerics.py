
import solvers.monte_carlo_multiple_initial_value as mcmiv


def do_config_mcmiv_100(dummy):
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 100
    return algorithm_mc


def do_config_mcmiv_1000(dummy):
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 1000
    return algorithm_mc
