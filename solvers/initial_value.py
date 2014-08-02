
import scipy.integrate

import common.utilities


'''
It calls odepack.lsoda to solve the initial value problem for stiff and non-stiff ode's
'''
def solve_lsoda_st(model, model_data, problem_data):
    model_data["parameters"] =  problem_data["parameters"]
    model_data["inputs"] = problem_data["inputs"]
    return scipy.integrate.odeint(
        func = model, \
        y0 = problem_data["initial_conditions"], \
        t = problem_data["time"], \
        args = (model_data["parameters"], model_data["inputs"]), \
        full_output = True, \
        printmessg = False, \
        ixpr = False)

'''
It computes the dynamic trajectory (or "time course") corresponding to the initial value problem
'''
def compute_trajectory_st(model, model_data, problem_data):
    trajectory_t, info = solve_lsoda_st(model, model_data, problem_data)
    trajectory = common.utilities.sliceit_assnapshot(trajectory_t)
    return trajectory
