
import scipy.integrate

import common.utilities
import common.diagnostics as cd

def handle_initial_point(values, problem_instance):
    if problem_instance["initial"] == "exclude":
        values = common.utilities.exclude_initial_point(values)
    return values


'''
Calls odepack.lsoda to solve the initial value problem for stiff and non-stiff ode's.
Preconditions: at this point in time, all problem-specific stuff must have been done;
this is a direct solver call and there is no context to do problem-specific things
'''
# TODO: deep copy?
def solve(model_data, problem_data):
    assert(len(problem_data["initial_conditions"]) == len(model_data["states"]))
    assert(model_data["states"] is not None)
    # TODO: preconditions
    # TODO: warnings
    # if problem_data != model_data, then warn

    # TODO: sort alphabetically
    return scipy.integrate.odeint(
        func        = model_data["model"], \
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
    # TODO: problem_data["initial"] not being handled correctly if called direction
    # TODO: preconditions

    if model is not None:
        assert(model is not None)
        model_data["model"] = model
        cd.print_legacy_code_message()

    snapshot, _ = solve(model_data, problem_data)
    return snapshot


'''
Computes the dynamic trajectories (or "time course") corresponding to the initial value problem.
It conditionally includes/excludes the initial point
'''
# TODO: return numpy.array()
# TODO: let problem_data count and use to override model_data
def compute_timecourse_trajectories(model, model_data, problem_data):
    # TODO: preconditions

    if model is not None:
        cd.print_legacy_code_message()
    
    snapshots = compute_trajectory_st(model, model_data, problem_data)
    including_initial_value = common.utilities.sliceit_astrajectory(snapshots)
    trajectories = handle_initial_point(including_initial_value, problem_data)

    return trajectories

# -----------------------------------------------------------------------------
'''
Legacy
'''
# -----------------------------------------------------------------------------
'''
Calls odepack.lsoda to solve the initial value problem for stiff and non-stiff ode's.
Preconditions: at this point in time, all problem-specific stuff must have been done;
this is a direct solver call and there is no context to do problem-specific things
'''
# TODO: remove when possible
# TODO: deep copy?
def solve_lsoda_st(model, model_data, problem_data):
    assert(len(problem_data["initial_conditions"]) == len(model_data["states"]))
    # TODO: preconditions

    cd.print_legacy_code_message()

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
