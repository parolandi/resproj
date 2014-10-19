
import data.generator as dg
import metrics.ordinary_differential as mod
import solvers.least_squares as sls
import solvers.solver_data as ss


montecarlo_multiple_optimisation_params = {
    "number_of_trials": 0,
    "decision_variable_ranges": [],
    "random_number_generator_seed": 117,
    "subsolver_params": dict(ss.algorithm_structure)
    }


montecarlo_multiple_optimisation_result = {
    "decision_variables": [],
    "success": [],
    }


# this does a montecarlo randomisation of initial guesses
# and solves the least-squares problem
def montecarlo_multiple_least_squares(model, problem, algorithm):
    assert(model["model"] is not None)
    # TODO: preconditions!
    
    multi_start_trials = algorithm["number_of_trials"]
    multi_start_points = []
    dv_count = len(algorithm["decision_variable_ranges"])
    for ii in range(dv_count):
        bounds = algorithm["decision_variable_ranges"][ii]
        dg.set_seed(algorithm["random_number_generator_seed"])
        points = dg.uniform_distribution(multi_start_trials)
        dg.unset_seed()
        scaled_points = bounds[0] + points * (bounds[1] - bounds[0]) 
        multi_start_points.append(scaled_points)

    result = dict(montecarlo_multiple_optimisation_result)
    subsolver_algorithm = dict(algorithm["subsolver_params"])
    for ii in range(multi_start_trials):
        initial_guesses = []
        for jj in range(dv_count):
            initial_guesses.append(multi_start_points[jj][ii])
        subsolver_algorithm["initial_guesses"] = initial_guesses
        trial_result = sls.solve_st( \
            mod.sum_squared_residuals_st, model["model"], model, problem, subsolver_algorithm)
        result["decision_variables"].append(trial_result.x)
        result["success"].append(trial_result.success)

    return result
