
import scipy.integrate

import common.utilities


def handle_initial_point(values, problem_instance):
    if problem_instance["initial"] == "exclude":
        values = common.utilities.exclude_initial_point(values)
    return values


'''
Calls odepack.lsoda to solve the initial value problem for stiff and non-stiff ode's.
Preconditions: at this point in time, all problem-specific stuff must have been done;
this is a direct solver call and there is no context to do problem-specific things
'''
# TODO: rename; remove lsoda_st
# TODO: deep copy?
def solve_lsoda_st(model, model_data, problem_data):
    assert(len(problem_data["initial_conditions"]) == len(model_data["states"]))
    # TODO: preconditions

    # TODO: sort alphabetically
    return scipy.integrate.odeint(
        func        = model, \
        y0          = problem_data["initial_conditions"], \
        # A sequence of time points for which to solve for y.
        # The initial value point should be the first element of this sequence.
        # http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html#scipy.integrate.odeint
        t           = problem_data["time"], \
        args        = (model_data["parameters"], model_data["inputs"]), \
        full_output = True, \
        printmessg  = False, \
        ixpr        = False)

'''
Computes the dynamic snapshots (or "time course") corresponding to the initial value problem.
Warning: it will unconditionally include the initial point
'''
# TODO: rename; "compute_timecourse_snapshots"
def compute_trajectory_st(model, model_data, problem_data):
    # TODO: preconditions
    snapshot, _ = solve_lsoda_st(model, model_data, problem_data)
    return snapshot


'''
Computes the dynamic trajectories (or "time course") corresponding to the initial value problem.
It conditionally includes/excludes the initial point
'''
# TODO: return numpy.array()
def compute_timecourse_trajectories(model, model_data, problem_data):
    # TODO: preconditions
    snapshots = compute_trajectory_st(model, model_data, problem_data)
    including_initial_value = common.utilities.sliceit_astrajectory(snapshots)
    trajectories = handle_initial_point(including_initial_value, problem_data)

    return trajectories
