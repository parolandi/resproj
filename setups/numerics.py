
import solvers.monte_carlo_multiple_initial_value as mcmiv
import solvers.nlp_interface as sonlin


def do_config_mcm_10(data):
    data["number_of_trials"] = 10
    return data


def do_config_mcm_100(data):
    data["number_of_trials"] = 100
    return data


def do_config_mcmls_nm(data):
    data["subsolver_params"]["method"] = "Nelder-Mead"
    return data


def do_config_mcmls_nlp(data):
    data["class"] = sonlin.somcmlesq.solve
    return data


def do_config_mcmiv_10(dummy):
    assert(dummy is None)
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 10
    return algorithm_mc


def do_config_mcmiv_100(dummy):
    assert(dummy is None)
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 100
    return algorithm_mc


def do_config_mcmiv_1000(dummy):
    assert(dummy is None)
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 1000
    return algorithm_mc


def do_config_mcmiv_100000(dummy):
    assert(dummy is None)
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 100000
    return algorithm_mc

def do_config_mcmiv_500000(dummy):
    assert(dummy is None)
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 500000
    return algorithm_mc

def do_config_mcmiv_250000(dummy):
    assert(dummy is None)
    algorithm_mc = dict(mcmiv.montecarlo_multiple_simulation_params)
    algorithm_mc["number_of_trials"] = 250000
    return algorithm_mc
